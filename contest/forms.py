from django import forms
from .models import Contest
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LangForm(forms.ModelForm):
    LANG = (('0', 'C'),
            ('1', 'C++'),
            ('2', 'Java'),
            ('3', 'Python'))

    lang = forms.MultipleChoiceField(
        widget=forms.SelectMultiple, choices=LANG, initial="1")


