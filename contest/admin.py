from django.contrib import admin
from .models import Contest, ConParticipants, ConProblems, ParticipantsSolved
from.forms import LangForm

# Register your models here.
class ConParticipantsAdmin(admin.StackedInline):
    model = ConParticipants
    extra = 1


class ConProblemsAdmin(admin.StackedInline):
    model = ConProblems
    extra = 1


class ContestAdmin(admin.ModelAdmin):
    form = LangForm
    search_fields = ['title']
    list_display = ['title', 'winner', 'start_time', 'end_time']
    inlines = [ConParticipantsAdmin, ConProblemsAdmin]


class ConParticipantsAdmin(admin.ModelAdmin):
    search_fields = ['contest']
    list_display = ['contest', 'participants']

class ConProblemsAdmin(admin.ModelAdmin):
    search_fields = ['contest']
    list_display = ['contest', 'problems']


class ParticipantsSolvedAdmin(admin.ModelAdmin):
    search_fields = ['contest']
    list_display = ['contest', 'problems', 'participants']

admin.site.register(Contest, ContestAdmin)
admin.site.register(ConParticipants, ConParticipantsAdmin)
admin.site.register(ConProblems, ConProblemsAdmin)
admin.site.register(ParticipantsSolved, ParticipantsSolvedAdmin)
