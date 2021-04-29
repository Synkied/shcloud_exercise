"""
Admin for users
"""
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating users. Includes all the fields on
    the user, plus a repeated password.
    """
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.is_active = True
        user.is_admin = False
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = (
        'email', 'name', 'is_active', 'is_admin', 'timezone',
    )
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email', 'name',)
    readonly_fields = ('private_key',)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (_('Credentials'), {
                    'fields': (
                        'email', 'password', 'private_key', 'is_active'
                    )
                }),
                (_('Flags'), {
                    'fields': (
                        'is_admin',
                    )
                }),
                (_('Personal information'), {'fields': (
                    'gender', 'name', 'timezone')}),
            )
        else:
            return (
                (_('Credentials'), {
                    'fields': (
                        'email', 'private_key', 'is_active'
                    )
                }),
                (_('Personal information'), {'fields': (
                    'gender', 'name', 'timezone',
                )}),
            )

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            kwargs['form'] = UserCreationForm

        self.instance = obj  # Keep the object for formfield_for_manytomany

        return super(UserAdmin, self).get_form(request, obj, **kwargs)
