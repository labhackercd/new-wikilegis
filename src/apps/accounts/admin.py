from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import UserProfile, ThematicGroup

admin.site.unregister(User)


class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True


class CustomUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


class CustomUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('profile')
    fk_name = 'user'
    raw_id_fields = ('themes',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = ((None, {'fields': ('username', 'email',
                                        'password1', 'password2'),
                             'classes': ('wide',)}),)
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


@admin.register(ThematicGroup)
class ThematicGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    list_filter = ('owner',)
    raw_id_fields = ('participants',)
    search_fields = ('name',)
