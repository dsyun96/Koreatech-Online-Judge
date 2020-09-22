from django.urls import path
from . import views

app_name = 'koj'

urlpatterns = [
    path('', views.index, name='index'),
    path('problemset', views.problemset, name='problemset'),
    path('problem/<int:prob_id>', views.problem_detail, name='problem_detail'),
    path('problem/create', views.problem_create, name='problem_create'),
    path('ranklist', views.ranklist, name='ranklist'),
    path('ide', views.ide, name='ide'),
    path('status', views.status, name='status'),
]
