from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Problem, Submit, Testcase
from common.models import CustomUser
from django.utils import timezone
# from django.contrib.auth.models import User
from .tasks import judge
from .forms import ProblemForm, TestcaseForm
from .infos import *


# Create your views here.
def index(request):
    return render(request, 'koj/index.html', {})


def problemset(request):
    page = request.GET.get('page', '1')  # 입력 파라미터
    problem_list = Problem.objects.order_by('prob_id')
    paginator = Paginator(problem_list, 15)  # 페이징 처리
    page_obj = paginator.get_page(page)

    problem_info = []
    for prob in problem_list[int(page) * 15 - 15: int(page) * 15]:
        problem_info.append((prob, Submit.objects.filter(problem=prob).filter(result=AC).count(),
                            Submit.objects.filter(problem=prob).count()))

    context = {'problem_list': page_obj, 'problems': problem_info}
    return render(request, 'koj/problemset.html', context)


def problem_detail(request, prob_id):
    problem = get_object_or_404(Problem, prob_id=prob_id)
    code = ''

    if request.GET.get('id'):
        # code = Submit.objects.all().filter(id=request.GET['id'])
        code = get_object_or_404(Submit, id=request.GET['id'])

    context = {'problem': problem, 'code': code}
    return render(request, 'koj/problem_detail.html', context)


def problem_write_for_user(request):
    if request.method == "GET":
        form = ProblemForm()
        form_t = TestcaseForm()

    if request.method == "POST":
        form = ProblemForm(request.POST)
        form_t = TestcaseForm(request.POST, request.FILES)

        if form.is_valid():
            user = CustomUser.objects.get(username=request.user.get_username())
            new_problem = Problem(
                prob_id=form.cleaned_data['prob_id'],
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                input=form.cleaned_data['input'],
                output=form.cleaned_data['output'],
                time_limit=form.cleaned_data['time_limit'],
                memory_limit=form.cleaned_data['memory_limit'],
                made_by=user
            )
            new_problem.save()

            if form_t.is_valid():
                temp_form = form_t.save(commit=False)
                temp_form.problem = Problem.objects.get(prob_id = new_problem.prob_id)
                temp_form.save()
                # form_t.input_data = Testcase(input_data = request.FILES['input_data'])
                # form_t.output_data = Testcase(output_data = request.FILES['output_data'])
                temp_form.save()
                return redirect('koj:problemset')

            # return redirect('koj:problem_write_addfile', new_problem.prob_id)
    # context = {'form':form, 'form_t':form_t}

    context = {'form_t': form_t, 'form': form}
    return render(request, 'koj/problem_write_for_user.html', context)


def problem_write_addfile(request, prob_id):
    if request.method == "GET":
        form = TestcaseForm()

    if request.method == "POST":
        form = TestcaseForm(request.POST, request.FILES)

        if form.is_valid():
            # form.save(commit=False)
            temp_form = form.save(commit=False)
            temp_form.problem = Problem.objects.get(prob_id=prob_id)
            temp_form.save()
            # form.problem = Problem.objects.get(prob_id = prob_id)
            # form.input_data = Testcase(input_data = request.FILES['input_data'])
            # form.output_data = Testcase(output_data = request.FILES['output_data'])
            return redirect('koj:index')

    context = {'form': form}
    return render(request, 'koj/problem_write_add_file.html', context)


def ranking_list(request):
    page = request.GET.get('page', '1')
    users = CustomUser.objects.all().order_by('rank')
    paginator = Paginator(users, 15)
    page_obj = paginator.get_page(page)

    context = {'Users_list': page_obj, 'Users': users[int(page) * 15 - 15: int(page) * 15]}
    return render(request, 'koj/ranking_list.html', context)


# ------------------------------------------------------------------------------------------------------------
def koj_ide(request):
    return render(request, 'koj/koj_ide.html')
# ------------------------------------------------------------------------------------------------------------



def status(request):
    if request.method == "POST":
        post_data = request.POST
        submit = Submit()
        submit.problem = Problem.objects.get(prob_id=post_data.get('prob_id'))
        submit.author = request.user
        submit.lang = post_data.get('lang')
        submit.code = post_data.get('code')
        submit.length = len(submit.code)
        submit.time = timezone.localtime()
        submit.save()
        judge.delay(submit.id)

    submits = Submit.objects.all().order_by('-id')

    if request.GET.get('user_id'):
        submits = submits.filter(author=CustomUser.objects.get(username=request.GET['user_id']))
    if request.GET.get('prob_id'):
        submits = submits.filter(problem=Problem.objects.get(prob_id=request.GET['prob_id']))
    if request.GET.get('result') == 'AC':
        submits = submits.filter(result=AC)
    if request.GET.get('result') == 'WA':
        submits = submits.filter(result=WA)

    page = request.GET.get('page', '1')
    paginator = Paginator(submits, 15)
    page_obj = paginator.get_page(page)

    submit_info = []
    for submit in submits[int(page) * 15 - 15: int(page) * 15]:
        submit_info.append((submit.id,
                            submit.author,
                            submit.problem,
                            submit_result[int(submit.result)] if submit.result is not None else '채점 중...',
                            submit.memory,
                            submit.runtime,
                            submit_lang[int(submit.lang)],
                            submit.length,
                            submit.time,
                            ))

    context = {'submit_list': page_obj, 'submits': submit_info}
    return render(request, 'koj/status.html', context)
