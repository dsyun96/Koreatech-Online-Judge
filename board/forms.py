from django import forms
from .models import Article, Comment
from django_summernote.widgets import SummernoteWidget


class ArticleForm(forms.ModelForm):
    HEAD_TYPES = [
        ('N', '자유'),
        ('Q', '질문'),
        ('I', '정보'),
    ]

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control item'}),
                            error_messages={'required': '제목을 입력해주세요'},
                            label='제목',
                            max_length=128
                            )
    # head =  forms.CharField(widget=forms.Select(choices=HEAD_TYPES))
    head = forms.ChoiceField(required=True,
                             label='분류',
                             choices=HEAD_TYPES,
                             )
    # content = forms.CharField(error_messages = {'required':"내용을 입력해주세요."}, label = "내용", widget = forms.Textarea)
    content = forms.CharField(error_messages={'required': '내용을 입력해주세요.'},
                              label='내용',
                              widget=SummernoteWidget()
                              )

    class Meta:
        model = Article
        fields = ['title', 'head', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '바르고 고운 말을 사용합시다', 'rows': 1}),
        }
