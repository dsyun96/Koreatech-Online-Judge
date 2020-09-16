from collections import namedtuple
import subprocess
import os
import fnmatch
import json
import _judger

Result = namedtuple('Result', 'result memory runtime')


class JudgeClass:
    DIR = '/Koreatech-OJ'
    no_exe = False

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
        print(os.listdir(os.getcwd()))
        if res:
            self.no_exe = True
        return res

    def __del__(self):
        print(os.listdir(os.getcwd()))
        os.system('rm {0}/Main*'.format(self.DIR))
        print(os.listdir(os.getcwd()))

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
        inputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(self.DIR, self._prob_id)), '*.in')
        outputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(self.DIR, self._prob_id)), '*.out')

        runtime = used_memory = 0
        for number in range(len(inputs)):
            with open(f'{self.DIR}/output', 'w') as out, open(f'{self.DIR}/error', 'w') as err:
                output_len = 0
                answer_data = []
                with open(f'{self.DIR}/upload/{self._prob_id}/{outputs[number]}', 'r') as answer:
                    for line in answer:
                        print(line)
                        output_len += len(line)
                        answer_data.append(line)

                res = _judger.run(max_cpu_time=self._time_limit * 1000,
                                  max_real_time=self._time_limit * 2000,
                                  max_memory=2048 * 2 ** 20,
                                  max_process_number=200,
                                  max_output_size=16384,
                                  max_stack=1024 * 1024 * 1024,
                                  exe_path=f"{self.run_cmd[self._lang]}",
                                  input_path=f"{self.DIR}/upload/{self._prob_id}/{inputs[number]}",
                                  output_path=f"{self.DIR}/output",
                                  error_path=f"{self.DIR}/error",
                                  seccomp_rule_name="c_cpp",
                                  args=[],
                                  env=[],
                                  log_path="judger.log",
                                  uid=0,
                                  gid=0
                                  )

                print(res)

                result = res['result']
                if 1 <= result <= 2:
                    return Result('TLE', -1, -1)
                elif result == 3:
                    return Result('MLE', -1, -1)
                elif result == 4:
                    if res['signal'] == 25:
                        return Result('PE', -1, -1)
                    if res['signal'] == 31:
                        pass  # system call
                    return Result('RE', -1, -1)
                elif result == 5:
                    return Result('ER', -1, -1)

                if not self.output_comparison(f'{self.DIR}/output', answer_data):
                    return Result('WA', -1, -1)

                runtime = max(runtime, res['cpu_time'])
                used_memory = max(used_memory, res['memory'])

        return Result('AC', used_memory // 1024 // 4 * 4, runtime // 4 * 4)


def judge_c(code, lang, prob_id, time_limit, memory_limit):
    judger = JudgeClass(code, lang, prob_id, time_limit, memory_limit)

    if judger.compile_check():
        return Result('CE', -1, -1)

    return judger.run()


def judge_cpp(code, lang, prob_id, time_limit, memory_limit):
    judger = JudgeClass(code, lang, prob_id, time_limit, memory_limit)

    if judger.compile_check():
        return Result('CE', -1, -1)

    return judger.run()


def judge_java(code, lang, prob_id, time_limit, memory_limit):
    judger = JudgeClass(code, lang, prob_id, time_limit, memory_limit)

    if judger.compile_check():
        return Result('CE', -1, -1)

    return judger.run()


def judge_python(submit):
    return Result('UC', -1, -1)
