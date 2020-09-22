from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Problem, Submit, Testcase, Language
from contest.models import Contest
from common.models import CustomUser
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .tasks import judge
from .forms import ProblemForm, TestcaseForm
from .infos import *


# Create your views here.
def index(request):
    return render(request, 'koj/index.html', {})


def problemset(request):
    page = request.GET.get('page', '1')  # 입력 파라미터
    problem_list = Problem.objects.filter(is_closed=False).order_by('prob_id')
    paginator = Paginator(problem_list, 15)  # 페이징 처리
    page_obj = paginator.get_page(page)

    problem_info = []
    for prob in problem_list[int(page) * 15 - 15: int(page) * 15]:
        problem_info.append((prob, Submit.objects.filter(problem=prob).filter(result=RESULT.AC).count(),
                             Submit.objects.filter(problem=prob).count()))

    context = {'problem_list': page_obj, 'problems': problem_info}
    return render(request, 'koj/problemset.html', context)


def problem_detail(request, prob_id):
    problem = get_object_or_404(Problem, prob_id=prob_id)
    code = ''
    cid = ''
    con_lang = ''

    if request.GET.get('id'):
        code = get_object_or_404(Submit, id=request.GET['id'])

    if request.GET.get('contest_id'):
        cid = request.GET.get('contest_id')
        con_lang = Contest.objects.get(contest_id=request.GET['contest_id']).lang

    examples = []
    for example in Testcase.objects.filter(problem=Problem.objects.get(prob_id=prob_id)).filter(is_example=True):
        with open(f'media/{example.input_data}', 'r') as input_file, \
                open(f'media/{example.output_data}', 'r') as output_file:
            examples.append(('\n'.join(input_file.readlines()), '\n'.join(output_file.readlines())))

    langs = []
    for lang in Language.objects.all():
        langs.append(lang)
    langs.sort(key=lambda x: x.name)

    context = {
        'problem': problem,
        'code': code,
        'examples': examples,
        'cid': cid,
        'con_lang': con_lang,
        'langs': langs
    }
    return render(request, 'koj/problem_detail.html', context)


@login_required(login_url='/common/login')
def problem_create(request):
    if request.method == "GET":
        form = ProblemForm()
        form_t = TestcaseForm()

    if request.method == "POST":
        print(request.POST.getlist('is_example'))
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
                made_by=user,
                is_closed=True
            )
            new_problem.save()

            if form_t.is_valid():
                for input_data, output_data, is_example in zip(
                        request.FILES.getlist('input_data'),
                        request.FILES.getlist('output_data'),
                        request.POST.getlist('example_flag')
                ):
                    testcase = Testcase(
                        problem=new_problem,
                        input_data=input_data,
                        output_data=output_data,
                        is_example=(is_example == '1')
                    )
                    testcase.save()
                return redirect('koj:problemset')

    context = {'form_t': form_t, 'form': form}
    return render(request, 'koj/problem_write_for_user.html', context)


def ranklist(request):
    page = request.GET.get('page', '1')
    users = CustomUser.objects.all()
    ranking_info = []

    for i in users[int(page) * 15 - 15: int(page) * 15]:
        submit_ac_d = Submit.objects.filter(author=i).filter(result=RESULT.AC).values('problem').distinct().count()
        submit_c = Submit.objects.filter(author=i).count()
        ranking_info.append((i, submit_ac_d, submit_c))

    ranking_info.sort(key=lambda x: -x[1])

    paginator = Paginator(users, 15)
    page_obj = paginator.get_page(page)

    context = {'Users_list': page_obj, 'ranking_info': ranking_info}
    return render(request, 'koj/ranking_list.html', context)


def ide(request):
    langs = []
    for lang in Language.objects.all():
        langs.append(lang)
    langs.sort(key=lambda x: x.name)

    return render(request, 'koj/ide.html', {
        'langs': langs
    })


def status(request):
    if request.method == "POST":
        post_data = request.POST
        submit = Submit()
        submit.problem = Problem.objects.get(prob_id=post_data.get('prob_id'))
        submit.author = request.user
        submit.lang = Language.objects.get(id=post_data.get('lang'))
        submit.code = post_data.get('code')
        submit.length = len(submit.code)
        submit.time = timezone.localtime()
        if post_data.get('cid'):
            submit.contest_id = post_data.get('cid')
            submit.for_contest = True
        submit.save()
        judge.delay(submit.id)

    submits = Submit.objects.all().order_by('-id')

    if request.GET.get('user_id'):
        submits = submits.filter(author=CustomUser.objects.get(username=request.GET['user_id']))
    if request.GET.get('prob_id'):
        submits = submits.filter(problem=Problem.objects.get(prob_id=request.GET['prob_id']))
    if request.GET.get('result'):
        submits = submits.filter(result=request.GET['result'])
    if request.GET.get('contest_id'):
        submits = submits.filter(for_contest=True)
    else:
        submits = submits.filter(for_contest=False)

    page = request.GET.get('page', '1')
    paginator = Paginator(submits, 15)
    page_obj = paginator.get_page(page)

    submit_info = []
    for submit in submits[int(page) * 15 - 15: int(page) * 15]:
        submit_info.append((
            submit.id,
            submit.author,
            submit.problem,
            results_ko[int(submit.result)] if submit.result is not None else '채점 중...',
            submit.memory,
            submit.runtime,
            submit.lang,
            submit.length,
            submit.time,
        ))

    context = {'submit_list': page_obj, 'submits': submit_info}
    return render(request, 'koj/status.html', context)
