from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from config import celery_app
from .models import Submit, Language, Testcase
from .infos import *
import subprocess
import os
import _judger
import shlex
import time


class Judge:

    def __init__(self, submit_id):
        self.DIR = f'judge/{submit_id}'
        self.channel_name = f'judge_{submit_id}'
        self.channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)(str(submit_id), self.channel_name)
        os.system(f'mkdir -p {self.DIR}')

        self.submit = Submit.objects.get(id=submit_id)
        self.submit.result = Submit.SubmitResult.ING
        async_to_sync(self.channel_layer.group_send)(
            str(self.submit.id), {
                'type': 'task_result',
                'result': f'{results_ko[self.submit.result]}',
                'id': self.submit.id
            }
        )

        self.problem = self.submit.problem
        self.lang = Language.objects.get(id=self.submit.lang.id)
        self.compile_option = []
        for arg in shlex.split(str(self.lang.compile_option)):
            idx = arg.find('Main')
            if idx == -1:
                self.compile_option.append(arg)
            else:
                self.compile_option.append(f'{arg[:idx]}{self.DIR}/{arg[idx:]}')

        with open(f'{self.DIR}/{self.lang.filename}', 'w') as f:
            f.write(self.submit.code)

    def __del__(self):
        async_to_sync(self.channel_layer.group_discard)(str(self.submit.id), self.channel_name)
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

        testcases = Testcase.objects.filter(problem=self.problem)
        testcase_count = testcases.count()

        for current, tc in enumerate(testcases, 1):
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
                    max_real_time=self.problem.time_limit * 10000,
                    max_memory=self.problem.memory_limit * 2 ** 20,
                    max_process_number=200,
                    max_output_size=max(1000, output_len * 2),
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
                args = []
                if str(self.lang) == 'Java':
                    args.append(f'-classpath')
                    args.append(f'{self.DIR}')

                for arg in shlex.split(str(self.lang.args)):
                    if str(self.lang) == 'Java' or 'Main' not in arg:
                        args.append(arg)
                    else:
                        idx = arg.find('Main')
                        args.append(f'{arg[:idx]}{self.DIR}/{arg[idx:]}')

                print(args)

                res = _judger.run(
                    max_cpu_time=self.problem.time_limit * 1000,
                    max_real_time=self.problem.time_limit * 2000,
                    max_memory=_judger.UNLIMITED if str(self.lang) == 'Java' else self.problem.memory_limit * 2 ** 20,
                    max_process_number=200,
                    max_output_size=max(1000, output_len * 2),
                    max_stack=_judger.UNLIMITED if str(self.lang) == 'Java' else self.problem.memory_limit * 2 ** 20,
                    exe_path=f'/usr/bin/{self.lang.exe}',
                    input_path=f'media/{tc.input_data}',
                    output_path=f'{self.DIR}/output',
                    error_path=f'{self.DIR}/error',
                    seccomp_rule_name=None if str(self.lang) == 'Java' else 'general',
                    args=args,
                    env=[],
                    log_path="judger.log",
                    uid=0,
                    gid=0
                )

            print(f'/usr/bin/{self.lang.exe}')
            print(f'media/{tc.input_data}')
            print(f'{self.DIR}/output')
            print(str(self.lang) == 'Java')
            print(res)

            result = res['result']
            if 1 <= result <= 2:
                return Submit.SubmitResult.TLE,
            elif result == 3:
                return Submit.SubmitResult.MLE,
            elif result == 4:
                if res['signal'] == 25:
                    return Submit.SubmitResult.OLE,
                if res['signal'] == 31:
                    pass  # system call
                return Submit.SubmitResult.RE,
            elif result == 5:
                return Submit.SubmitResult.ER,

            if not self.answer_check(answer_data):
                return Submit.SubmitResult.WA,

            runtime = max(runtime, res['cpu_time'])
            used_memory = max(used_memory, res['memory'])
            async_to_sync(self.channel_layer.group_send)(
                str(self.submit.id), {
                    'type': 'task_result',
                    'result': f'채점 중 ({current * 100 // testcase_count}%)',
                    'id': self.submit.id
                }
            )

        return Submit.SubmitResult.AC, runtime // 4 * 4, used_memory // 4096 * 4


class Run:

    def __init__(self, code, langid, data):
        self.DIR = f'run/{time.time()}'
        os.system(f'mkdir -p {self.DIR}')

        self.lang = Language.objects.get(id=langid)
        self.compile_option = []
        for unit in shlex.split(str(self.lang.compile_option)):
            idx = unit.find('Main')
            if idx == -1:
                self.compile_option.append(unit)
            else:
                self.compile_option.append(f'{unit[:idx]}{self.DIR}/{unit[idx:]}')

        with open(f'{self.DIR}/{self.lang.filename}', 'w') as f:
            f.write(code)

        with open(f'{self.DIR}/input', 'w') as f:
            f.write(data)

    def __del__(self):
        os.system(f'rm -rf {self.DIR}')

    def compile(self):
        return subprocess.call(self.compile_option)

    def run(self):
        res = None
        if str(self.lang) == 'C' or str(self.lang) == 'C++':
            res = _judger.run(
                max_cpu_time=1000,
                max_real_time=2000,
                max_memory=128 * 2 ** 20,
                max_process_number=200,
                max_output_size=131072,
                max_stack=128 * 2 ** 20,
                exe_path=f'{self.DIR}/{self.lang.exe}',
                input_path=f'{self.DIR}/input',
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
            args = []
            if str(self.lang) == 'Java':
                args.append(f'-classpath')
                args.append(f'{self.DIR}')

            for arg in shlex.split(str(self.lang.args)):
                if str(self.lang) == 'Java' or 'Main' not in arg:
                    args.append(arg)
                else:
                    idx = arg.find('Main')
                    args.append(f'{arg[:idx]}{self.DIR}/{arg[idx:]}')

            print(args)

            res = _judger.run(
                max_cpu_time=1000,
                max_real_time=2000,
                max_memory=_judger.UNLIMITED if str(self.lang) == 'Java' else 128 * 2 ** 20,
                max_process_number=200,
                max_output_size=131072,
                max_stack=_judger.UNLIMITED if str(self.lang) == 'Java' else 128 * 2 ** 20,
                exe_path=f'/usr/bin/{self.lang.exe}',
                input_path=f'{self.DIR}/input',
                output_path=f'{self.DIR}/output',
                error_path=f'{self.DIR}/error',
                seccomp_rule_name=None if str(self.lang) == 'Java' else 'general',
                args=args,
                env=[],
                log_path="judger.log",
                uid=0,
                gid=0
            )

        output = ''
        with open(f'{self.DIR}/output', 'r') as f:
            output = ''.join(f.readlines())

        return output


@celery_app.task
def judge(submit_id):
    channel_layer = get_channel_layer()
    channel_name = f'pre_judge_{submit_id}'
    judge_object = Judge(submit_id)

    def _disconnect():
        async_to_sync(channel_layer.group_discard)(str(submit_id), channel_name)

    if judge_object.compile():
        async_to_sync(channel_layer.group_send)(
            str(submit_id), {
                'type': 'task_result',
                'result': f'{results_ko[Submit.SubmitResult.CE]}',
                'id': submit_id
            }
        )
        judge_object.submit.result = Submit.SubmitResult.CE
        judge_object.submit.save()
        _disconnect()
        return

    judge_res = judge_object.run()

    if judge_res[0] == Submit.SubmitResult.AC:
        judge_object.submit.result, judge_object.submit.runtime, judge_object.submit.memory = judge_res
    else:
        judge_object.submit.result = judge_res[0]

    async_to_sync(channel_layer.group_send)(
        str(submit_id), {
            'type': 'task_result',
            'result': f'{results_ko[judge_object.submit.result]}',
            'id': submit_id,
            'memory': judge_object.submit.memory,
            'runtime': judge_object.submit.runtime,
        }
    )
    judge_object.submit.save()
    _disconnect()


@shared_task
def run(channel_name, code, langid, data):
    run_object = Run(code, langid, data)

    if run_object.compile():
        return

    result = run_object.run()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name, {
            'output': result,
            'type': 'task_result',
        }
    )
