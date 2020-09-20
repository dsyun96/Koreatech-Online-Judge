from django.shortcuts import render, get_object_or_404, redirect
from koj.models import Problem, Testcase, Submit
from django.core.paginator import Paginator
from .models import Contest, ConParticipants, ConProblems
from django.conf import settings
from koj.infos import *


# Create your views here.
def contest_list(request):
    contest = Contest.objects.all().order_by('contest_id')
    context = {'contest': contest}
    return render(request, 'contest/contest_list.html', context)


def contest_detail(request, contest_id):
    # prob = Contest.objects.values_list('Problems', 'p_list')

    contest = get_object_or_404(Contest, contest_id=contest_id)
    contest_probs = ConProblems.objects.filter(contest=contest)
    contest_partis = ConParticipants.objects.filter(contest=contest)

    problem_info = []
    for prob in contest_probs:
        # number = contest_probs.values_list('problems', flat=True)
        problem_info.append((Problem.objects.get(prob_id=prob.problems.prob_id),
                             Submit.objects.filter(problem=prob.problems).filter(result=AC).count(),
                             Submit.objects.filter(problem=prob.problems).count()))

    context = {'con': contest,
               'con_prob': contest_probs,
               'con_partis': contest_partis,
               'problem_info': problem_info
               }

    return render(request, 'contest/contest.html', context)
