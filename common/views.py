from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from koj.models import Problem, Submit
from .forms import CustomUserCreationForm
from koj.infos import *


class signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('common:signup_success')
    template_name = 'common/signup.html'


def user_detail(request, username):
    user = CustomUser.objects.get(username=username)
    context = {'User': user}
    return render(request, 'common/user_detail.html', context)


def user_problem(request, username):
    """나중에 사용자가 많아지면 CustomUser 모델에 맞은 문제 리스트, 각 결과의 개수, 랭크 등을 관리할 예정"""

    user = CustomUser.objects.get(username=username)
    submits = Submit.objects.filter(author=user).values('problem', 'result')

    counts = [0] * len(results_en)
    for submit in submits:
        counts[submit['result']] += 1

    tried_problems = submits.values_list('problem', flat=True).distinct()

    ac_problems = submits.filter(result=RESULT.AC).values_list('problem', flat=True).distinct()
    wa_problems = tried_problems.difference(ac_problems)

    rank = 1
    for other in CustomUser.objects.all():
        other_submits = Submit.objects.filter(author=other)
        other_ac_problems = other_submits.values_list('problem', flat=True).distinct()
        if ac_problems.count() < other_ac_problems.count() or \
           ac_problems.count() == other_ac_problems.count() and submits.count() > other_submits.count():
            rank += 1

    ac_problems_id = []
    for i in ac_problems:
        ac_problems_id.append(Problem.objects.get(id=i))

    wa_problems_id = []
    for i in wa_problems:
        wa_problems_id.append(Problem.objects.get(id=i))

    context = {
        **{results_en[e]: res for e, res in enumerate(counts)},
        **{
            'User': user,
            'ac_problems': ac_problems_id,
            'wa_problems': wa_problems_id,
        },
        'rank': rank,
        'solved': ac_problems.count(),
        'submit': submits.count()
    }

    return render(request, 'common/user_problem.html', context)
