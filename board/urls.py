from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('article_list', views.article_list, name='article_list'),
    path('article_write', views.article_write, name='article_write'),
    path('article/<int:article_id>', views.article_detail, name='article_detail'),
    path('article_update/<int:article_id>', views.article_update, name='article_update'),
    path('article_delete/<int:article_id>', views.article_delete, name='article_delete'),
    path('article_rcmd/<int:article_id>', views.article_rcmd, name='article_rcmd'),
    path('comment_write/<int:article_id>', views.comment_write, name='comment_write'),
    path('comment_delete/<int:com_id>/<int:article_id>', views.comment_delete, name='comment_delete'),
]
