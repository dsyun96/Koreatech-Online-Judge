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
    user = CustomUser.objects.get(username=username)

    submit_ac_d = Submit.objects.filter(author=user).filter(result=RESULT.AC). \
        order_by('problem').values('problem').distinct()

    s_ac = Submit.objects.filter(author=user).filter(result=RESULT.AC).values('problem').distinct()
    
    s_wa = Submit.objects.filter(author=user).filter(result=RESULT.WA).values('problem').distinct()
    submit_wa_d = s_wa.difference(s_ac)

    submit_ac_c = Submit.objects.filter(author=user).filter(result=RESULT.AC).count()
    submit_ac_d_c = submit_ac_d.count()
    submit_wa_c = Submit.objects.filter(author=user).filter(result=RESULT.WA).count()
    submit_c = Submit.objects.filter(author=user).count()

    submit_tle_c = Submit.objects.filter(author=user).filter(result=RESULT.TLE).count()
    submit_mle_c = Submit.objects.filter(author=user).filter(result=RESULT.MLE).count()
    submit_ole_c = Submit.objects.filter(author=user).filter(result=RESULT.OLE).count()
    submit_ce_c = Submit.objects.filter(author=user).filter(result=RESULT.CE).count()
    submit_re_c = Submit.objects.filter(author=user).filter(result=RESULT.RE).count()


    ranking = CustomUser.objects.all()
    counts = 1

    for i in ranking:
        k = Submit.objects.filter(author=i).filter(result=RESULT.AC).values('problem').distinct().count()
        if submit_ac_d_c < k:
            counts += 1

    submit_list_ac_e = []
    submit_list_wa_e = []

    for i in submit_ac_d:
        submit_list_ac_e.append(Problem.objects.get(pk=list(i.values())[0]))

    for i in submit_wa_d:
        submit_list_wa_e.append(Problem.objects.get(pk=list(i.values())[0]))

    user_submits = []
    user_submits.append((counts, submit_ac_d_c, submit_c, submit_ac_c, submit_wa_c,
                         submit_tle_c, submit_ole_c, submit_mle_c, submit_ce_c, submit_re_c))

    context = {
        'User': user,
        'submits_ac_d': submit_list_ac_e,
        'submits_wa': submit_list_wa_e,
        'user_submits': user_submits,
    }

    return render(request, 'common/user_problem.html', context)
