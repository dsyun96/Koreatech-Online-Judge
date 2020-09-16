from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm


class signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('common:signup_success')
    template_name = 'common/signup.html'



"""
def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('koj:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
"""
