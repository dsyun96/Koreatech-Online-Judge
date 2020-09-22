from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from config import celery_app
from .models import Submit, Language, Testcase
from .runs import *
import subprocess
import os
from .infos import RESULT
import _judger


class Judge:

    def __init__(self, submit_id):
        self.DIR = f'judge/{submit_id}'
        os.system(f'mkdir -p {self.DIR}')

        self.submit = Submit.objects.get(id=submit_id)
        self.problem = self.submit.problem
        self.lang = Language.objects.get(id=self.submit.lang.id)
        self.compile_option = []
        for unit in self.lang.compile_option.split():
            if 'Main' in unit:
                self.compile_option.append(f'{self.DIR}/{unit}')
            else:
                self.compile_option.append(unit)

        print(self.compile_option)
        with open(f'{self.DIR}/{self.lang.filename}', 'w') as f:
            f.write(self.submit.code)

    def __del__(self):
        os.system(f'rm -rf {self.DIR}')

    def compile(self):
        return subprocess.call(self.compile_option)

    def answer_check(self, answer):
        with open(f'{self.DIR}/output', 'r') as output:
            user_output = output.readlines()

            while len(user_output) and not user_output[-1].rstrip():
                user_output.pop()
            while len(answer) and not answer[-1].rstrip():
                answer.pop()

            if len(user_output) != len(answer):
                return False

            for line in range(len(user_output)):
                if user_output[line].rstrip() != answer[line].rstrip():
                    return False

        return True

    def run(self):
        runtime = 0
        used_memory = 0

        for tc in Testcase.objects.filter(problem=self.problem):
            output_len = 0
            answer_data = []
            with open(f'media/{tc.output_data}', 'r') as answer:
                for line in answer:
                    output_len += len(line)
                    answer_data.append(line)

            res = None
            if str(self.lang) == 'C' or str(self.lang) == 'C++':
                res = _judger.run(
                    max_cpu_time=self.problem.time_limit * 1000,
                    max_real_time=self.problem.time_limit * 2000,
                    max_memory=self.problem.memory_limit * 2 ** 20,
                    max_process_number=200,
                    max_output_size=output_len*2,
                    max_stack=self.problem.memory_limit * 2 ** 20,
                    exe_path=f'{self.DIR}/{self.lang.exe}',
                    input_path=f'media/{tc.input_data}',
                    output_path=f'{self.DIR}/output',
                    error_path=f'{self.DIR}/error',
                    seccomp_rule_name='c_cpp',
                    args=[],
                    env=[],
                    log_path=f'{self.DIR}/judger.log',
                    uid=0,
                    gid=0
                )
            else:
                res = _judger.run(
                    max_cpu_time=self.problem.time_limit * 1000,
                    max_real_time=self.problem.time_limit * 2000,
                    max_memory=_judger.UNLIMITED if self.lang == 'Java' else self.problem.memory_limit * 2 ** 20,
                    max_process_number=200,
                    max_output_size=max(100, output_len * 2),
                    max_stack=_judger.UNLIMITED if self.lang == 'Java' else self.problem.memory_limit * 2 ** 20,
                    exe_path=f'/usr/bin/{self.lang.exe}',
                    input_path=f'media/{tc.input_data}',
                    output_path=f'{self.DIR}/output',
                    error_path=f'{self.DIR}/error',
                    seccomp_rule_name=None if self.lang == 'Java' else 'general',
                    args=[f'{self.DIR}/' + unit if 'Main' in unit else unit for unit in self.lang.args.split()],
                    env=[],
                    log_path="judger.log",
                    uid=0,
                    gid=0
                )

            result = res['result']
            if 1 <= result <= 2:
                return RESULT.TLE,
            elif result == 3:
                return RESULT.MLE,
            elif result == 4:
                if res['signal'] == 25:
                    return RESULT.OLE,
                if res['signal'] == 31:
                    pass  # system call
                return RESULT.RE,
            elif result == 5:
                return RESULT.ER,

            if not self.answer_check(answer_data):
                return RESULT.WA,

            runtime = max(runtime, res['cpu_time'])
            used_memory = max(used_memory, res['memory'])

        return RESULT.AC, runtime // 4 * 4, used_memory // 4096 * 4


@celery_app.task
def judge(submit_id):
    judge_object = Judge(submit_id)

    if judge_object.compile():
        judge_object.submit.result = RESULT.CE
        judge_object.submit.save()
        return

    judge_res = judge_object.run()

    if judge_res[0] == RESULT.AC:
        judge_object.submit.result, judge_object.submit.runtime, judge_object.submit.memory = judge_res
    else:
        judge_object.submit.result = judge_res[0]

    judge_object.submit.save()


@shared_task
def run(channel_name, code, lang, input_data):
    run_func = [run_c, judge_cpp, judge_java, judge_python, ]

    with open('test_input', 'w') as f:
        f.write(input_data)

    result = run_func[int(lang)](code, lang)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name, {
            'message': result,
            'type': 'task_result',
        }
    )
