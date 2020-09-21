from django.contrib import admin
from .models import Problem, Testcase, Submit
from django_summernote.admin import SummernoteModelAdmin


class TestcaseAdmin(admin.StackedInline):
    model = Testcase
    extra = 1


class ProblemAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ['prob_id', 'title', 'time_limit', 'memory_limit', 'made_by']
    list_display_links = ['prob_id', 'title']
    list_filter = ('made_by', )
    search_fields = ['title', 'prob_id']
    inlines = [TestcaseAdmin]


class TestcaseAdmin(admin.ModelAdmin):
    list_display = ['get_prob_id', 'get_prob_title', 'is_example']
    search_fields = ['problem__title', 'problem__prob_id']

    def get_prob_id(self, obj):
        return obj.problem.prob_id
    get_prob_id.short_description = '문제 번호'

    def get_prob_title(self, obj):
        return obj.problem.title
    get_prob_title.short_description = '제목'


class SubmitAdmin(admin.ModelAdmin):
    list_display = [
        'get_author',
        'get_prob_id',
        'get_prob_title',
        'result',
        'memory',
        'runtime',
        'lang',
        'length',
        'contest_id',
    ]

    def get_prob_id(self, obj):
        return obj.problem.prob_id
    get_prob_id.short_description = '문제 번호'

    def get_prob_title(self, obj):
        return obj.problem.title
    get_prob_title.short_description = '제목'

    def get_author(self, obj):
        return obj.author.get_username()
    get_author.short_description = '아이디'


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Testcase, TestcaseAdmin)
admin.site.register(Submit, SubmitAdmin)
