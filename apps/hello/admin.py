from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User


class HelloUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class HelloUserAdmin(UserAdmin):
    form = HelloUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',
                                      'birthday', 'bio')}),
        ('Contacts', {'fields': ('contact_jabber', 'contact_skype',
                                 'othercontacts')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )


admin.site.register(User, HelloUserAdmin)
