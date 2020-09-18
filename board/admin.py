from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    search_fields = ['title']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
