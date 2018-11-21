from django.contrib import admin

from .models import UserProfile, ThematicGroup


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'profile_type',
        'gender',
        'uf',
        'country',
        'birthdate',
        'avatar',
    )
    list_filter = ('user', 'birthdate')
    raw_id_fields = ('themes',)


@admin.register(ThematicGroup)
class ThematicGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    list_filter = ('owner',)
    raw_id_fields = ('participants',)
    search_fields = ('name',)
