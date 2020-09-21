from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from koj.models import Problem, Testcase, Submit
from .forms import CustomUserCreationForm
from koj.infos import *


class signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('common:signup_success')
    template_name = 'common/signup.html'


def user_detail(request, username):
    # user_id = request.session.get('user_id')
    # user = CustomUser.objects.get(username = request.user.get_username())

    user_id = get_object_or_404(CustomUser, username=username)
    user = CustomUser.objects.get(username=username)
    submit = Submit()

    submit_ac_d = Submit.objects.filter(author=user).filter(result=AC).\
        order_by('problem').values('problem').distinct()

    s_ac = Submit.objects.filter(author=user).filter(result=AC).values('problem').distinct()
    s_wa = Submit.objects.filter(author=user).filter(result=WA).values('problem').distinct()
    submit_wa_d = s_wa.difference(s_ac)

    submit_ac_c = Submit.objects.filter(author=user).filter(result=AC).count()
    submit_ac_d_c = submit_ac_d.count()
    submit_wa_c = Submit.objects.filter(author=user).filter(result=WA).count()
    submit_c = Submit.objects.filter(author=user).count()

    ranking = CustomUser.objects.all()
    counts = 1

    for i in ranking:
        k = Submit.objects.filter(author=i).filter(result=AC).values('problem').distinct().count()
        if submit_ac_d_c < k :
            counts += 1

    submit_list_ac_e = []
    submit_list_wa_e = []

    for i in submit_ac_d:
        submit_list_ac_e.append(Problem.objects.get(pk=list(i.values())[0]))

    for i in submit_wa_d:
        submit_list_wa_e.append(Problem.objects.get(pk=list(i.values())[0]))

    context = {'User': user,
               'submits_ac_d': submit_list_ac_e,
               'submits_wa': submit_list_wa_e,
               'submits_count_ac_d': submit_ac_d_c,
               'submits_count_wa': submit_wa_c,
               'submit_count_author': submit_c,
               'submits_count_ac': submit_ac_c,
               'user_rank': counts,
               }

    return render(request, 'common/user_detail.html', context)


"""
def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('koj:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
"""
