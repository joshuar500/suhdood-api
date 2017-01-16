from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from suhdood.models.account import Account
from suhdood.models.share import Share
from suhdood.models.url import Url


class AccountCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'display_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AccountCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'display_name', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AccountAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base AccountAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'display_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Display Name', {'fields': ('display_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. AccountAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'display_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class ShareAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'shared_url', 'date', 'viewed')
    raw_id_fields = ('sender', 'receiver')

class UrlCreationForm(forms.ModelForm):
    url = forms.CharField(label='Url', widget=forms.URLInput)    

    class Meta:
        model = Url
        exclude = ('hashed_url', 'url_string')

    def save(self, commit=True):
        url = super(UrlCreationForm, self).save(commit=False)
        url.hashed_url = url.hash_url(self.cleaned_data["url"])
        url.url_string = self.cleaned_data["url"]
        if commit:
            url.save()
        return url

class UrlAdmin(admin.ModelAdmin):
    form = UrlCreationForm
    list_display = ('hashed_url', 'url_string')

# Now register the new models...
admin.site.register(Account, AccountAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Url, UrlAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)