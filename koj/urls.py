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
    path('ranking_list', views.ranking_list, name='ranking_list'),
    path('ide', views.ide, name='ide'),
    path('status', views.status, name='status'),
    path('test', views.test, name='test'),
]
