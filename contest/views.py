from django.shortcuts import render, get_object_or_404, redirect
from koj.models import Problem, Testcase, Submit
from django.core.paginator import Paginator
from .models import Contest, ConProblem
from django.conf import settings
from koj.infos import *


# Create your views here.
def contest_list(request):
    contest = Contest.objects.all().order_by('contest_id')
    context = {'contest': contest}
    return render(request, 'contest/contest_list.html', context)


def contest_detail(request, contest_id):

    contest = get_object_or_404(Contest, contest_id=contest_id)
    contest_prob = ConProblem.objects.filter(contest=contest).order_by('conp_id')
    contest_parti = contest.participant

    problem_info = []
    for con in contest_prob:
        problem = Problem.objects.get(prob_id=con.problem.prob_id)
        problem_solved = Submit.objects.filter(problem=problem).filter(result=RESULT.AC).filter(for_contest=True).count()
        problem_submitted = Submit.objects.filter(problem=problem).filter(for_contest=True).count()

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

    context = {'con': contest,
               'con_prob': contest_prob,
               }
    return render(request, 'contest/contest_ranking.html', context)