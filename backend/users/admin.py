from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User

    ordering = ('phone_number',)
    list_editable = ('other_invite_code',)
    list_display = (
        'id',
        'phone_number',
        'invite_code',
        'other_invite_code',)
