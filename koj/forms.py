from django import forms
from .models import Article, Comment, Problem, prob_path, Testcase
from common.models import CustomUser
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ArticleForm(forms.ModelForm):
    HEAD_TYPES = [('N', '자유'),
                    ('Q', '질문'),
                    ('I', '정보'),
            ]
    title = forms.CharField(error_messages = {'required':"제목을 입력해주세요"}, label = "제목", max_length=128)
    #head =  forms.CharField(widget=forms.Select(choices=HEAD_TYPES))
    head = forms.ChoiceField(required=True, choices=HEAD_TYPES)
    #content = forms.CharField(error_messages = {'required':"내용을 입력해주세요."}, label = "내용", widget = forms.Textarea)
    content = forms.CharField(error_messages = {'required':"내용을 입력해주세요."}, label = "내용", widget = CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = ['title','head','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
          'content': forms.Textarea(attrs={'placeholder': '바르고 고운 말을 사용합시다', 'rows':1}),
        }

class ProblemForm(forms.ModelForm):
    prob_id = forms.IntegerField(label = "문제 번호")
    title = forms.CharField(label = "제목")
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
