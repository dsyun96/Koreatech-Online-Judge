from django.contrib import admin
from django import forms
from .models import Problem, Testcase, Submit, Contest, ConParticipants, ConProblems


class TestcaseAdmin(admin.StackedInline):
    model = Testcase


class ProblemAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [TestcaseAdmin]


class Con_Participants(admin.StackedInline):
    model = ConParticipants


class Con_Problems(admin.StackedInline):
    model = ConProblems


class ContestAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [Con_Participants, Con_Problems]
    # inlines = [Con_Problems]


class TestcaseAdmin(admin.ModelAdmin):
    pass


class Con_Participants(admin.ModelAdmin):
    pass


class Con_Problems(admin.ModelAdmin):
    pass


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Testcase, TestcaseAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Submit)
