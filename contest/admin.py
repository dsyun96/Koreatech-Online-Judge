from django.contrib import admin
from .models import Contest, ConParticipants, ConProblems

# Register your models here.

class Con_Participants(admin.StackedInline):
    model = ConParticipants


class Con_Problems(admin.StackedInline):
    model = ConProblems


class ContestAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [Con_Participants, Con_Problems]


class Con_Participants(admin.ModelAdmin):
    pass


class Con_Problems(admin.ModelAdmin):
    pass


admin.site.register(Contest, ContestAdmin)
