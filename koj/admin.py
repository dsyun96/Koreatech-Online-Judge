from django.contrib import admin
from .models import Problem, Testcase, Submit
from django_summernote.admin import SummernoteModelAdmin


class TestcaseAdmin(admin.StackedInline):
    model = Testcase


class ProblemAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    search_fields = ['title']
    inlines = [TestcaseAdmin]


class TestcaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Testcase, TestcaseAdmin)
admin.site.register(Submit)
