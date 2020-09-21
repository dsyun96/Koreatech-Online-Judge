from django.contrib import admin
from .models import Contest, ParticipantsSolved
from.forms import LangForm

# Register your models here.


class ContestAdmin(admin.ModelAdmin):
    form = LangForm
    search_fields = ['title']
    list_display = ['title', 'winner', 'start_time', 'end_time']
    filter_horizontal = ['problem']


class ParticipantsSolvedAdmin(admin.ModelAdmin):
    search_fields = ['contest']
    list_display = ['contest', 'problems', 'participants']


admin.site.register(Contest, ContestAdmin)
admin.site.register(ParticipantsSolved, ParticipantsSolvedAdmin)
