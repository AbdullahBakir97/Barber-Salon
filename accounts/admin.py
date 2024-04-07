from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, OwnerProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'date_of_birth', 'gender', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('password',)  

class OwnerProfileAdmin(admin.ModelAdmin):
    model = OwnerProfile

admin.site.register(UserProfile)
admin.site.register(OwnerProfile, OwnerProfileAdmin)
