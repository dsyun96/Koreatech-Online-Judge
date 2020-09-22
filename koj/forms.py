from django import forms
from .models import Problem, Testcase
from django_summernote.widgets import SummernoteWidget


class ProblemForm(forms.ModelForm):
    prob_id = forms.IntegerField(label='문제 번호')
    title = forms.CharField(label='제목')

    body = forms.CharField(
        label='본문',
        widget=SummernoteWidget()
    )
    input = forms.CharField(
        label='입력',
        widget=SummernoteWidget()
    )
    output = forms.CharField(
        label='출력',
        widget=SummernoteWidget()
    )

    time_limit = forms.IntegerField(label='시간 제한 (초)')
    memory_limit = forms.IntegerField(label='메모리 제한 (MB)')

    class Meta:
        model = Problem
        fields = ['prob_id', 'title', 'body', 'input', 'output', 'time_limit', 'memory_limit']


class TestcaseForm(forms.ModelForm):
    is_example = forms.BooleanField(label='예시로 쓸까요?', required=False)
    example_flag = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Testcase
        fields = ['input_data', 'output_data', 'is_example', 'example_flag']
