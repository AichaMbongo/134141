from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Profile, CustomUser
admin.site.unregister(Group)

admin.site.unregister(User)
class ProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
       
    )

# Register the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
     


# admin.site.register(User, UserAdmin)