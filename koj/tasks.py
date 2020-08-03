from config import celery_app
from .models import Submit
import subprocess
import os
import fnmatch

DIR = '/home/dsyun/grad/projects/mysite'

filename = [
    'Main.c',
    'Main.cc',
    'Main.java',
    'Main.py'
]
compile_cmd = [
    ['gcc', '{0}/{1}'.format(DIR, filename[0]), '-o', '{0}/Main'.format(DIR), '-O2', '-lm', '-std=c99'],
    ['g++', '{0}/{1}'.format(DIR, filename[1]), '-o', '{0}/Main'.format(DIR), '-O2', '-lm', '-std=gnu++98'],
    ['javac', '-J-Xms1024m', '-J-Xmx1024m', '-J-Xss512m', '-encoding', 'UTF-8', '{0}/{1}'.format(DIR, filename[2])],
    ['python3', '-c', '"import py_compile; py_compile.compile(r\'Main.py\')"']
]
run_cmd = [
    ['{0}/Main'.format(DIR)],
    ['{0}/Main'.format(DIR)],
    ['java', '-Xms1024m', '-Xmx1024m', '-Xss512m', '-Dfile.encoding=UTF-8', '{0}/Main'.format(DIR)],
    ['python3', 'Main.py']
]


@celery_app.task
def judge(submit_id):
    result = ''
    submit = Submit.objects.get(id=submit_id)

    with open('{0}/{1}'.format(DIR, filename[int(submit.lang)]), 'w') as f:
        f.write(submit.code)

    if subprocess.call(compile_cmd[int(submit.lang)]) != 0:
        result = 'CE'
    else:
        inputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.in')
        outputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.out')

        def correct(o1, file):
            o1 = o1.decode().rstrip().split('\n')
            o2 = ''
            with open('{0}/upload/{1}/{2}'.format(DIR, submit.problem.prob_id, file), 'r') as f:
                for line in f:
                    o2 += line + '\n'

            o2 = o2.rstrip().split('\n')

            if len(o1) != len(o2):
                return False

            for i in range(len(o1)):
                if o1[i].rstrip() != o2[i]:
                    return False

            return True

        for i in range(len(inputs)):
            with open('{0}/upload/{1}/{2}'.format(DIR, submit.problem.prob_id, inputs[i])) as stdin:
                try:
                    print('a' * 50)
                    output = subprocess.check_output(run_cmd[int(submit.lang)], stdin=stdin, timeout=1)
                    print('b' * 50)
                    if not correct(output, outputs[i]):
                        result = 'WA'
                        break
                except subprocess.TimeoutExpired:
                    result = 'TLE'
                    break
                except Exception as ex:
                    result = 'RE'
                    print(ex)
                    break
        else:
            result = 'AC'

    submit.result = result
    submit.save()
