from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model


# Register your models here.
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    search_fields = ['title']
    list_display = ['get_author', 'head', 'title', 'views', 'recommend', 'created_at', 'ip_address']
    list_display_links = ['title']

    def get_author(self, obj):
        return obj.author.get_username()
    get_author.short_description = '아이디'


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']
    list_display = ['get_author', 'article', 'content', 'created_at']
    list_display_links = ['content']

    def get_author(self, obj):
        return obj.author.get_username()
    get_author.short_description = '아이디'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(get_attachment_model())
