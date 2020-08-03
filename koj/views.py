from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Problem, Submit
from django.utils import timezone
from django.contrib.auth.models import User
from .tasks import judge


# Create your views here.
def index(request):
    return render(request, 'koj/index.html', {})


def problemset(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')

    # 조회
    problem_list = Problem.objects.order_by('prob_id')

    # 페이징 처리
    paginator = Paginator(problem_list, 15)
    page_obj = paginator.get_page(page)

    context = {'problem_list': page_obj, 'problems': problem_list[int(page) * 15 - 15: int(page) * 15]}
    return render(request, 'koj/problemset.html', context)


def problem_detail(request, prob_id):
    problem = get_object_or_404(Problem, prob_id=prob_id)
    context = {'problem': problem}
    return render(request, 'koj/problem_detail.html', context)


def status(request):
    if request.method == "POST":
        POST_data = request.POST
        submit = Submit()
        submit.problem = Problem.objects.get(prob_id=POST_data.get('prob_id'))
        submit.author = request.user
        submit.lang = POST_data.get('lang')
        submit.code = POST_data.get('code')
        submit.length = len(submit.code)
        submit.time = timezone.localtime()
        submit.save()
        judge.delay(submit.id)

    submit_list = Submit.objects.all().order_by('-id')

    if request.GET.get('user_id'):
        submit_list = submit_list.filter(author=User.objects.get(username=request.GET['user_id']))
    if request.GET.get('prob_id'):
        submit_list = submit_list.filter(problem=Problem.objects.get(prob_id=request.GET['prob_id']))

    page = request.GET.get('page', '1')
    paginator = Paginator(submit_list, 15)
    page_obj = paginator.get_page(page)

    context = {'submit_list': page_obj, 'submits': submit_list[int(page) * 15 - 15: int(page) * 15]}
    return render(request, 'koj/status.html', context)
