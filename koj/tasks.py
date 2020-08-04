from config import celery_app
from .models import Submit
from .judges import *


@celery_app.task
def judge(submit_id):
    submit = Submit.objects.get(id=submit_id)
    language = int(submit.lang)
    judge_func = [judge_c, judge_cpp, judge_java, judge_python, ]

    with open('{0}/{1}'.format(DIR, filename[language]), 'w') as f:
        f.write(submit.code)

    judge_result = judge_func[language](submit)

    os.remove('{0}/{1}'.format(DIR, filename[language]))

    submit.result = judge_result['result']
    submit.memory = judge_result['memory']
    submit.runtime = judge_result['runtime']
    submit.save()
