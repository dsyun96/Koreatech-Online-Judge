from django.shortcuts import render, get_object_or_404, redirect
from koj.models import Problem, Testcase, Submit
from django.core.paginator import Paginator
from .models import Contest, ConProblem
from django.conf import settings
from koj.infos import *
from datetime import datetime
from django.utils import timezone



# Create your views here.
def contest_list(request):
    contest = Contest.objects.all().order_by('contest_id')
    context = {'contest': contest}
    return render(request, 'contest/contest_list.html', context)


def contest_detail(request, contest_id):
    contest = get_object_or_404(Contest, contest_id=contest_id)
    contest_prob = ConProblem.objects.filter(contest=contest).order_by('conp_id')


    problem_info = []
    for con in contest_prob:
        problem = Problem.objects.get(prob_id=con.problem.prob_id)
        problem_solved = Submit.objects.filter(problem=problem).filter(result=Submit.SubmitResult.AC).filter(contest_id=contest.contest_id).count()
        problem_submitted = Submit.objects.filter(problem=problem).filter(contest_id=contest.contest_id).count()

        problem_info.append((problem, problem_solved, problem_submitted))



    """
    if contest.private:
        is_available = 0
        for i in contest_partis:
            if request.user == i.participants:
                is_available = 1
    else:
        is_available = 1
    """
    context = {'con': contest,
               'problem_info': problem_info,
               # 'is_available':is_available,
               }

    return render(request, 'contest/contest.html', context)


def contest_ranking(request, contest_id):
    contest = get_object_or_404(Contest, contest_id=contest_id)
    contest_prob = ConProblem.objects.filter(contest=contest).order_by('conp_id')
    contest_parti = contest.participant
    con_submit = Submit.objects.filter(contest_id=contest_id)

    date_str = "2099-12-31 23:59:59"
    date_str2 = "00:01:00"
    date_str3 = "00:02:00"

    contest_ranking = []

    contest_start = contest.start_time
    standard = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    standard = timezone.make_aware(standard)

    penalty_time = timezone.make_aware(datetime.strptime(date_str3, '%H:%M:%S')) \
                    - timezone.make_aware(datetime.strptime(date_str2, '%H:%M:%S'))
    penalty_time = penalty_time * contest.penalty


    for con in contest_parti.all():
        con_submits = con_submit.filter(author=con)
        contest_solved_t = []
        solved_time_sum = []
        wrong_sum = 0
        time = contest_start - contest_start
        time_sum = contest_start - contest_start
        for prob in contest_prob:
            solved_submits = con_submits.filter(problem=prob.problem).filter(result=0)
            wrong_submits = con_submits.filter(problem=prob.problem).filter(result__range=(1, 8))
            is_solved = False
            wrongs = 0

            solved_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            solved_time = timezone.make_aware(solved_time)

            for solved in solved_submits:
                if solved.time < solved_time:
                    is_solved = True
                    solved_time = solved.time
                    time_sum += solved_time - contest_start

            for wrong in wrong_submits:
                wrongs += 1

            if solved_time == standard:
                solved_time = None

            if is_solved:
                wrong_sum += wrongs

            contest_solved_t.append((solved_time, wrongs))

        solved_count = con_submits.filter(result=0).values_list('problem', flat=True).distinct().count()

        time_sum = time_sum + (penalty_time * wrong_sum)

        contest_ranking.append((con, solved_count, contest_solved_t, time_sum))

        contest_ranking.sort(key=lambda x: (-x[1], x[3]))

    context = {'con': contest,
               'con_prob': contest_prob,
               'contest_ranking': contest_ranking,
               'penalty_time': penalty_time,
               }
    return render(request, 'contest/contest_ranking.html', context)