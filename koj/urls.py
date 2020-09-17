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
    path('problem_write_for_user', views.problem_write_for_user, name='problem_write_for_user'),
    path('problem_write_addfile/<int:prob_id>', views.problem_write_addfile, name='problem_write_addfile'),
    path('ranking_list', views.ranking_list, name='ranking_list'),
    path('koj_ide', views.koj_ide, name='koj_ide'),
    path('user_detail/<str:username>', views.user_detail, name='user_detail'),
    path('contest_list', views.contest_list, name='contest_list'),
    path('contest/<int:contest_id>', views.contest_detail, name='contest_detail'),

    path('status', views.status, name='status'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
