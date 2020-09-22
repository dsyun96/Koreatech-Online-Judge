from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'contest'

urlpatterns = [
    path('contest_list', views.contest_list, name='contest_list'),
    path('contest_detail/<int:contest_id>', views.contest_detail, name='contest_detail'),
path('contest_ranking/<int:contest_id>', views.contest_ranking, name='contest_ranking'),
]
