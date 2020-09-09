from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Problem, Submit, Article, Comment, Fortest
from common.models import CustomUser
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .tasks import judge
from .forms import ArticleForm, CommentForm


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

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
def koj_ide(request):
    return render(request, 'koj/koj_ide.html')
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def article_list(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')

    # 조회
    article_list = Article.objects.order_by('article_id')

    # 페이징 처리
    paginator = Paginator(article_list, 10)
    page_obj = paginator.get_page(page)

    context = {'article_list': page_obj, 'articles': article_list[int(page) * 10 - 10 : int(page) * 10]}
    return render(request, 'koj/article_list.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comment = CommentForm()
    context = {'article': article, 'comment':comment}
    session_cookie = request.session.get('user_id')
    cookie_name = F'notice_hits:{session_cookie}'

    response = render(request, 'koj/article_detail.html', context)

    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(article_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{article_id}', expires=None)
            article.views += 1
            article.save()
            return response
    else:
        response.set_cookie(cookie_name, article_id, expires=None)
        article.views += 1
        article.save()
        return response

    return render(request, 'koj/article_detail.html', context)

@login_required
def article_write(request):
    if request.method == "GET":
        form = ArticleForm()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    if request.method == "POST":
        form = ArticleForm(request.POST)

        if form.is_valid():
            user_id = request.session.get('user_id')
            user = CustomUser.objects.get(username = request.user.get_username())
            new_article = Article(
                title = form.cleaned_data['title'],
                head = form.cleaned_data['head'],
                content = form.cleaned_data['content'],
                author = user,
                ip_address = ipaddress
            )
            new_article.save()
            #messages.success(request, '성공적으로 등록되었습니다.')
            return redirect('koj:article_list')

    return render(request, 'koj/article_write.html', {'form' :form})


def article_update(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)

    if article.author != request.user.username:
       messages.error(request, '작성자가 아니면 수정할 수 없습니다!')
       return redirect('/article/' + str(article.article_id))

    if request.method == 'POST':
        form = ArticleForm(request.POST or None, instance=article)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            #article.title = form.cleaned_data['title'],
            #article.head = form.cleaned_data['head'],
            #article.content = form.cleaned_data['content'],
            #article.created_at =timezone.now()
            #article.save()
            messages.success(request, '성공적으로 수정되었습니다.')
            return redirect('/article/' + str(article.article_id))

    else :
        form = ArticleForm(instance=article)
        return render(request, 'koj/article_update.html', {'form':form})

@login_required
def article_delete(request, article_id):
     article = get_object_or_404(Article, article_id=article_id)

     if article.author != request.user.username:
         messages.error(request, '작성자가 아니면 삭제할 수 없습니다!')
         return redirect('/article/' + str(article.article_id))

     article.delete()
     return redirect('koj:article_list')


def article_rcmd(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    context = {'article': article}
    session_cookie = request.session.get('user_id')
    cookie_name = F'recomended:{session_cookie}'

    response = render(request, 'koj/article_detail.html', context)

    if request.COOKIES.get(cookie_name) is not None:
        messages.error(request, '여러번 추천할 수 없습니다!!')
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(article_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{article_id}', expires=None)
            article.rcmd += 1
            article.save()
            return response
    else:
        #messages.error(request, '여러번 추천할 수 없습니다!')
        response.set_cookie(cookie_name, article_id, expires=None)
        article.rcmd += 1
        article.save()
        return response
    return redirect('/article/' + str(article.article_id))


def comment_write(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    filled_form = CommentForm(request.POST)
    user = CustomUser.objects.get(username = request.user.get_username())
    if filled_form.is_valid():
        temp_form = filled_form.save(commit=False)
        temp_form.article = Article.objects.get(article_id = article_id)
        temp_form.author = user
        temp_form.save();

        return redirect('/article/' + str(article.article_id))


def comment_delete(request, com_id, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    if article.author != request.user.username:
        messages.error(request, '작성자가 아니면 삭제할 수 없습니다!')
        return redirect('/article/' + str(article.article_id))


    mycom = Comment.objects.get(id = com_id)
    mycom.delete()
    return redirect('/article/' + str(article.article_id))

def user_detail(request, username):
    #user_id = request.session.get('user_id')
    #user = CustomUser.objects.get(username = request.user.get_username())

    user_id = get_object_or_404(CustomUser, username = username)
    user = CustomUser.objects.get(username = username)
    submit = Submit()

    submit_list_ac_d = Submit.objects.filter(author=user).filter(result='AC').order_by('problem').values('problem').distinct()


    submit_ac = Submit.objects.filter(author=user).filter(result='AC').values('problem').distinct()
    submit_wa = Submit.objects.filter(author=user).filter(result='WA').values('problem').distinct()
    submit_list_wa_d = submit_wa.difference(submit_ac)


    submit_count_ac = Submit.objects.filter(author=user).filter(result='AC').count()
    submit_count_ac_d = submit_list_ac_d.count()
    submit_count_wa = Submit.objects.filter(author=user).filter(result='WA').count()
    submit_count_author = Submit.objects.filter(author=user).count()


    submit_list_ac_e = []
    submit_list_wa_e = []


    for i in submit_list_ac_d:
        submit_list_ac_e.append(Problem.objects.get(pk=list(i.values())[0]))

    for i in submit_list_wa_d:
        submit_list_wa_e.append(Problem.objects.get(pk=list(i.values())[0]))


    context = {'User': user, 'submits_ac_d':submit_list_ac_e, 'submits_count_ac_d':submit_count_ac_d,
        'submits_wa':submit_list_wa_e, 'submits_count_wa':submit_count_wa, 'submit_count_author':submit_count_author,
        'submits_count_ac':submit_count_ac}

    return render(request, 'koj/user_detail.html', context)


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
        submit_list = submit_list.filter(author=CustomUser.objects.get(username=request.GET['user_id']))
    if request.GET.get('prob_id'):
        submit_list = submit_list.filter(problem=Problem.objects.get(prob_id=request.GET['prob_id']))
    if request.GET.get('result')=='AC':
        submit_list = submit_list.filter(result='AC')
    if request.GET.get('result')=='WA':
        submit_list = submit_list.filter(result='WA')


    if request.GET.get('result')=='WA_d':
        submit_list = submit_list.filter(result='WA')

    page = request.GET.get('page', '1')
    paginator = Paginator(submit_list, 15)
    page_obj = paginator.get_page(page)


    context = {'submit_list': page_obj, 'submits': submit_list[int(page) * 15 - 15: int(page) * 15]}
    return render(request, 'koj/status.html', context)
