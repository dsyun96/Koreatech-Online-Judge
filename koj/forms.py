from django import forms
from .models import Problem, Testcase


class ProblemForm(forms.ModelForm):
    prob_id = forms.IntegerField(label='문제 번호')
    title = forms.CharField(label='제목')
    body = forms.CharField()
    input = forms.CharField()
    output = forms.CharField()
    time_limit = forms.IntegerField()
    memory_limit = forms.IntegerField()

    class Meta:
        model = Problem
        fields = ['prob_id', 'title', 'body', 'input', 'output', 'time_limit', 'memory_limit']


class TestcaseForm(forms.ModelForm):
    class Meta:
        model = Testcase
        fields = ['input_data', 'output_data']
