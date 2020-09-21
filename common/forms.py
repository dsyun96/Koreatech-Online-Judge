from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control item'})
        }
        labels = {
            'username' : 'ID'
        }
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control item'}), label= 'Passwrod')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control item'}), label= 'Confirm Password')

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control item'}), label= 'E - mail')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'gender', 'birth_date')
