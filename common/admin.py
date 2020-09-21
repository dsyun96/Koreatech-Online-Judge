from django.contrib import admin
from .models import CustomUser
from.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


# Register your models here.
class CustomUserAdmin(UserAdmin):
    # fieldsets : 관리자 리스트 화면에서 출력될 폼 설정 부분
    UserAdmin.fieldsets[0][1]['fields'] += ('major', 'freetext')
    # add_fieldsets : User 객체 추가 화면에 출력될 입력 폼 설정 부분
    UserAdmin.add_fieldsets += (
        ('Additional Info', {'fields': ('major', 'freetext')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
