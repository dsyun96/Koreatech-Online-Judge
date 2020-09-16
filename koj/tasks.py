from config import celery_app
from .models import Submit
from .judges import *


@celery_app.task
def judge(submit_id):
    submit = Submit.objects.get(id=submit_id)
    problem = submit.problem
    lang = int(submit.lang)
    judge_func = [judge_c, judge_cpp, judge_java, judge_python, ]

    res = judge_func[lang](submit.code, lang, problem.prob_id, problem.time_limit, problem.memory_limit)

    submit.result = res.result
    submit.memory = res.memory
    submit.runtime = res.runtime
    submit.save()
