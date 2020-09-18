from .models import Testcase, Problem
from collections import namedtuple
import subprocess
import os
import fnmatch
import json
import _judger
from .infos import *

Result = namedtuple('Result', 'result memory runtime')


class JudgeClass:
    DIR = '/Koreatech-OJ'
    filename = [
        'Main.c',
        'Main.cc',
        'Main.java',
        'Main.py',
    ]
    compile_cmd = [
        ['gcc', '{0}/{1}'.format(DIR, filename[0]), '-o', '{0}/Main'.format(DIR), '-O2', '-lm', '-std=c99'],
        ['g++', '{0}/{1}'.format(DIR, filename[1]), '-o', '{0}/Main'.format(DIR), '-O2', '-lm', '-std=gnu++98'],
        ['javac', '-J-Xms1024m', '-J-Xmx1024m', '-J-Xss512m', '-encoding', 'UTF-8', '{0}/{1}'.format(DIR, filename[2])],
        ['python3', '-c', '"import py_compile; py_compile.compile(r\'{0}/{1}\')"'.format(DIR, filename[3])],
    ]
    run_cmd = [
        f'{DIR}/Main',
        f'{DIR}/Main',
        f'{DIR}/java_runner',
        f'',
    ]

    def __init__(self, code, lang, prob_id, time_limit, memory_limit):
        self._lang = lang
        self._prob_id = prob_id
        self._time_limit = time_limit
        self._memory_limit = memory_limit

        with open('{0}/{1}'.format(self.DIR, self.filename[self._lang]), 'w') as f:
            f.write(code)

    def compile_check(self):
        res = subprocess.call(self.compile_cmd[int(self._lang)])
        # print(os.listdir(os.getcwd()))
        return res

    def __del__(self):
        # print(os.listdir(os.getcwd()))
        os.system('rm {0}/Main*'.format(self.DIR))
        # print(os.listdir(os.getcwd()))

    def output_comparison(self, o1, answer):
        with open(o1, 'r') as f1:
            user_output = f1.readlines()

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
        testcases = Testcase.objects.filter(problem=Problem.objects.get(prob_id=self._prob_id))

        runtime = used_memory = 0
        for tc in testcases:
            output_len = 0
            answer_data = []
            with open(f'{self.DIR}/media/{tc.output_data}', 'r') as answer:
                for line in answer:
                    output_len += len(line)
                    answer_data.append(line)

            res = _judger.run(
                max_cpu_time=self._time_limit * 1000,
                max_real_time=self._time_limit * 2000,
                max_memory=self._memory_limit * 2 ** 20,
                max_process_number=200,
                max_output_size=max(100, output_len * 2),
                max_stack=self._memory_limit * 2 ** 20,
                exe_path=f"{self.run_cmd[self._lang]}",
                input_path=f"{self.DIR}/media/{tc.input_data}",
                output_path=f"{self.DIR}/output",
                error_path=f"{self.DIR}/error",
                seccomp_rule_name="c_cpp",
                args=[],
                env=[],
                log_path="judger.log",
                uid=0,
                gid=0
            )

            result = res['result']
            if 1 <= result <= 2:
                return Result(TLE, -1, -1)
            elif result == 3:
                return Result(MLE, -1, -1)
            elif result == 4:
                if res['signal'] == 25:
                    return Result(OLE, -1, -1)
                if res['signal'] == 31:
                    pass  # system call
                return Result(RE, -1, -1)
            elif result == 5:
                return Result(ER, -1, -1)

            if not self.output_comparison(f'{self.DIR}/output', answer_data):
                return Result(WA, -1, -1)

            runtime = max(runtime, res['cpu_time'])
            used_memory = max(used_memory, res['memory'])

        return Result(AC, used_memory // 1024 // 4 * 4, runtime // 4 * 4)


def judge_c(code, lang, prob_id, time_limit, memory_limit):
    judger = JudgeClass(code, lang, prob_id, time_limit, memory_limit)

    if judger.compile_check():
        return Result(CE, -1, -1)

    return judger.run()


def judge_cpp(code, lang, prob_id, time_limit, memory_limit):
    judger = JudgeClass(code, lang, prob_id, time_limit, memory_limit)

    if judger.compile_check():
        return Result(CE, -1, -1)

    return judger.run()


def judge_java(code, lang, prob_id, time_limit, memory_limit):
    judger = JudgeClass(code, lang, prob_id, time_limit, memory_limit)

    if judger.compile_check():
        return Result(CE, -1, -1)

    return judger.run()


def judge_python(submit):
    return Result(-1, -1, -1)
