from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'common'

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.signup.as_view(), name='signup'),
    path('signup_success', TemplateView.as_view(template_name='common/signup_success.html'), name='signup_success'),
]
