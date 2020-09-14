from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'koj'

urlpatterns = [
    path('', views.index, name='index'),
    path('problemset', views.problemset, name='problemset'),
    path('problem/<int:prob_id>', views.problem_detail, name='problem_detail'),
    path('problem_write_foruser/', views.problem_write_foruser, name='problem_write_foruser'),
    path('problem_write_addfile/<int:prob_id>', views.problem_write_addfile, name='problem_write_addfile'),
    path('ranking_list/', views.ranking_list, name='ranking_list'),
    path('koj_ide', views.koj_ide, name='koj_ide'),
    path('article_list/', views.article_list, name='article_list'),
    path('article_write/', views.article_write, name='article_write'),
    path('article/<int:article_id>', views.article_detail, name='article_detail'),
    path('article_update/<int:article_id>', views.article_update, name='article_update'),
    path('article_delete/<int:article_id>', views.article_delete, name='article_delete'),
    path('article_rcmd/<int:article_id>', views.article_rcmd, name='article_rcmd'),
    path('comment_write/<int:article_id>', views.comment_write , name='comment_write'),
    path('comment_delete/<int:com_id>/<int:article_id>',views.comment_delete , name='comment_delete'),
    path('user_detail/<str:username>', views.user_detail , name='user_detail'),

    path('status', views.status, name='status'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
