from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from common.models import CustomUser
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from koj.infos import *

# Create your views here.
def article_list(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')

    # 조회
    articles = Article.objects.order_by('article_id')

    # 페이징 처리
    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(page)

    context = {'article_list': page_obj, 'articles': articles[int(page) * 10 - 10: int(page) * 10]}
    return render(request, 'board/article_list.html', context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comment = CommentForm()
    context = {'article': article, 'comment': comment}
    session_cookie = request.session.get('user_id')
    cookie_name = f'notice_hits:{session_cookie}'

    response = render(request, 'board/article_detail.html', context)

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

    return render(request, 'board/article_detail.html', context)


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
            user = CustomUser.objects.get(username=request.user.get_username())
            new_article = Article(
                title=form.cleaned_data['title'],
                head=form.cleaned_data['head'],
                content=form.cleaned_data['content'],
                author=user,
                ip_address=ipaddress
            )
            new_article.save()
            # messages.success(request, '성공적으로 등록되었습니다.')
            return redirect(reverse('board:article_list'))

    return render(request, 'board/article_write.html', {'form': form})


def article_update(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)

    if article.author != request.user.username:
        messages.error(request, '작성자가 아니면 수정할 수 없습니다!')
        return redirect(reverse('board:article_detail', args=(article.article_id,)))

    if request.method == 'POST':
        form = ArticleForm(request.POST or None, instance=article)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # article.title = form.cleaned_data['title'],
            # article.head = form.cleaned_data['head'],
            # article.content = form.cleaned_data['content'],
            # article.created_at =timezone.now()
            # article.save()
            messages.success(request, '성공적으로 수정되었습니다.')
            return redirect(reverse('board:article_detail', args=(article.article_id,)))

    else:
        form = ArticleForm(instance=article)
        return render(request, 'board/article_update.html', {'form': form})


@login_required
def article_delete(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)

    if article.author != request.user.username:
        messages.error(request, '작성자가 아니면 삭제할 수 없습니다!')
        return redirect(reverse('board:article_detail', args=(article.article_id,)))

    article.delete()
    return redirect(reverse('board:article_list'))


def article_rcmd(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    context = {'article': article}
    session_cookie = request.session.get('user_id')
    cookie_name = f'recomended:{session_cookie}'

    response = render(request, 'board/article_detail.html', context)

    if request.COOKIES.get(cookie_name) is not None:
        messages.error(request, '여러번 추천할 수 없습니다!!')
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(article_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{article_id}', expires=None)
            article.recommend += 1
            article.save()
            return response
    else:
        # messages.error(request, '여러번 추천할 수 없습니다!')
        response.set_cookie(cookie_name, article_id, expires=None)
        article.recommend += 1
        article.save()
        return response
    return redirect(reverse('board:article_detail', args=(article.article_id,)))


def comment_write(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    filled_form = CommentForm(request.POST)
    user = CustomUser.objects.get(username=request.user.get_username())
    if filled_form.is_valid():
        temp_form = filled_form.save(commit=False)
        temp_form.article = Article.objects.get(article_id=article_id)
        temp_form.author = user
        temp_form.save()

        return redirect(reverse('board:article_detail', args=(article.article_id,)))


def comment_delete(request, com_id, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    if article.author != request.user.username:
        messages.error(request, '작성자가 아니면 삭제할 수 없습니다!')
        return redirect(reverse('board:article_detail', args=(article.article_id,)))

    mycom = Comment.objects.get(id=com_id)
    mycom.delete()
    return redirect(reverse('board:article_detail', args=(article.article_id,)))
