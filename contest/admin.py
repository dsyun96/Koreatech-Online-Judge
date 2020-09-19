from django.contrib import admin
from .models import Contest, ConParticipants, ConProblems


# Register your models here.
class ConParticipantsAdmin(admin.StackedInline):
    model = ConParticipants
    extra = 1


class ConProblemsAdmin(admin.StackedInline):
    model = ConProblems
    extra = 1


class ContestAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'winner', 'start_time', 'end_time']
    inlines = [ConParticipantsAdmin, ConProblemsAdmin]


admin.site.register(Contest, ContestAdmin)
