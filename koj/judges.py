import subprocess
import os
import fnmatch

DIR = '/home/dsyun/grad/projects/mysite'

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
    ['{0}/Main'.format(DIR)],
    ['{0}/Main'.format(DIR)],
    ['java', '-Xms1024m', '-Xmx1024m', '-Xss512m', '-Dfile.encoding=UTF-8', '{0}/Main'.format(DIR)],
    ['python3', '{0}/{1}'.format(DIR, filename[3])],
]


def correct(o1, file, prob_id):
    o1 = o1.decode().rstrip().split('\n')
    o2 = ''
    with open('{0}/upload/{1}/{2}'.format(DIR, prob_id, file), 'r') as f:
        for line in f:
            o2 += line + '\n'

    o2 = o2.rstrip().split('\n')

    if len(o1) != len(o2):
        return False

    for i in range(len(o1)):
        if o1[i].rstrip() != o2[i]:
            return False

    return True


def judge_c(submit):
    ret = dict()
    result, memory, runtime = '', -1, -1

    if subprocess.call(compile_cmd[int(submit.lang)]) != 0:
        result = 'CE'
    else:
        inputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.in')
        outputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.out')

        for i in range(len(inputs)):
            with open('{0}/upload/{1}/{2}'.format(DIR, submit.problem.prob_id, inputs[i])) as stdin:
                try:
                    output = subprocess.check_output(run_cmd[int(submit.lang)], stdin=stdin, timeout=1)
                    if not correct(output, outputs[i], submit.problem.prob_id):
                        result = 'WA'
                        break
                except subprocess.TimeoutExpired:
                    result = 'TLE'
                    break
                except:
                    result = 'RE'
                    break
        else:
            result = 'AC'

        os.remove('{0}/Main'.format(DIR))

    ret['result'] = result
    ret['memory'] = memory
    ret['runtime'] = runtime
    return ret


def judge_cpp(submit):
    ret = dict()
    result, memory, runtime = '', -1, -1

    if subprocess.call(compile_cmd[int(submit.lang)]) != 0:
        result = 'CE'
    else:
        inputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.in')
        outputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.out')

        for i in range(len(inputs)):
            with open('{0}/upload/{1}/{2}'.format(DIR, submit.problem.prob_id, inputs[i])) as stdin:
                try:
                    output = subprocess.check_output(run_cmd[int(submit.lang)], stdin=stdin, timeout=1)
                    if not correct(output, outputs[i], submit.problem.prob_id):
                        result = 'WA'
                        break
                except subprocess.TimeoutExpired:
                    result = 'TLE'
                    break
                except:
                    result = 'RE'
                    break
        else:
            result = 'AC'

        os.remove('{0}/Main'.format(DIR))

    ret['result'] = result
    ret['memory'] = memory
    ret['runtime'] = runtime
    return ret


def judge_java(submit):
    ret = dict()
    result, memory, runtime = '', -1, -1

    if subprocess.call(compile_cmd[int(submit.lang)]) != 0:
        result = 'CE'
    else:
        inputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.in')
        outputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.out')

        for i in range(len(inputs)):
            with open('{0}/upload/{1}/{2}'.format(DIR, submit.problem.prob_id, inputs[i])) as stdin:
                try:
                    output = subprocess.check_output(run_cmd[int(submit.lang)], stdin=stdin, timeout=1)
                    if not correct(output, outputs[i], submit.problem.prob_id):
                        result = 'WA'
                        break
                except subprocess.TimeoutExpired:
                    result = 'TLE'
                    break
                except:
                    result = 'RE'
                    break
        else:
            result = 'AC'

        os.remove('{0}/Main.class'.format(DIR))

    ret['result'] = result
    ret['memory'] = memory
    ret['runtime'] = runtime
    return ret


def judge_python(submit):
    ret = dict()
    result, memory, runtime = '', -1, -1

    if subprocess.call(compile_cmd[int(submit.lang)]) != 0:
        result = 'CE'
    else:
        inputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.in')
        outputs = fnmatch.filter(os.listdir('{0}/upload/{1}'.format(DIR, submit.problem.prob_id)), '*.out')

        for i in range(len(inputs)):
            with open('{0}/upload/{1}/{2}'.format(DIR, submit.problem.prob_id, inputs[i])) as stdin:
                try:
                    output = subprocess.check_output(run_cmd[int(submit.lang)], stdin=stdin, timeout=1)
                    if not correct(output, outputs[i], submit.problem.prob_id):
                        result = 'WA'
                        break
                except subprocess.TimeoutExpired:
                    result = 'TLE'
                    break
                except:
                    result = 'RE'
                    break
        else:
            result = 'AC'

        os.remove('{0}/Main.py'.format(DIR))

    ret['result'] = result
    ret['memory'] = memory
    ret['runtime'] = runtime
    return ret
