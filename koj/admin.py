from django.contrib import admin
from django import forms
from .models import Problem, Testcase, Submit


class TestcaseAdmin(admin.StackedInline):
    model = Testcase


class ProblemAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [TestcaseAdmin]


class TestcaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Testcase, TestcaseAdmin)
admin.site.register(Submit)
