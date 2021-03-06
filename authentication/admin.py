import logging

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser, Client
from .utils import get_sales_contact_from_admin_request

logger = logging.getLogger(__name__)

"""
Some modifications to support custom user in admin.
"""


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'mobile')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format and set the attribute is_staff to True
        :param commit:
        :return: an instance of the user.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'mobile')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    def group(self, user):
        """
        Shows groups of a user.
        :param user: The user of which we want to know the group he is part of.
        :return: A string with all groups of the user.
        """
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    list_display = (
        'email', 'first_name', 'last_name', 'phone', 'mobile', 'is_superuser',
        'is_staff', 'group', 'date_created', 'date_updated')
    list_filter = ('is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'mobile')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'mobile', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'mobile')
    ordering = ('email',)
    filter_horizontal = ()


class ClientAdmin(admin.ModelAdmin):
    """
    Custom client admin, handling admin page for clients.
    """
    list_display = (
        'first_name', 'last_name', 'email', 'sales_contact', 'phone', 'mobile', 'company_name', 'date_created', 'date_updated')
    search_fields = ('first_name', 'last_name', 'email', 'company_name', 'sales_contact')

    def get_actions(self, request):
        """
        Overrides get_actions of ModelAdmin to implement removal of delete actions in admin list view for non superusers.
        :param request: The HTML request.
        :return: a list of actions
        """
        actions = super().get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        """
        Overrides get_readonly_fields of ModelAdmin to implement deactivation of modification of fields in
        admin detailed view for non-authorized users, as only superusers and sales_contact of a client are
        authorized to modify it.
        :param request: The HTML request.
        :return: A list of read only fields.
        """
        read_only_fields = super().get_readonly_fields(request)
        try:
            sales_contact = get_sales_contact_from_admin_request(request)
            if request.user != sales_contact and not request.user.is_superuser:
                read_only_fields = read_only_fields + (
                    'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'date_created',
                    'date_updated', 'sales_contact')
        except KeyError:
            logger.warning("User tried to access a client page that does not exist.")
        return read_only_fields

    def has_delete_permission(self, request, obj=None):
        """
        Overrides get_readonly_fields of ModelAdmin to implement deactivation of delete button in admin detailed view
        for non-authorized users, as only superusers and sales_contact of a client are authorized to modify it.
        :param request: The HTML request.
        :return: A boolean determining if the user has permission to delete.
        """
        if request.resolver_match.url_name == 'authentication_client_change':
            try:
                sales_contact = get_sales_contact_from_admin_request(request)
                return request.user == sales_contact or request.user.is_superuser
            except KeyError:
                logger.warning("User tried to access a client page that does not exist.")
        return super().has_delete_permission(request)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Client, ClientAdmin)
