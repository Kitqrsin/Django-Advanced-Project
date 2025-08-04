from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):

    # Additional safety for non-superusers not altering superusers

    def has_delete_permission(self, request, obj = None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


    def has_change_permission(self, request, obj = None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    # Prevent non-superusers from seeing superusers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs


    # prevent non-superusers from changing is_superuser with UI
    def get_form(
            self, request, obj=None, change=None, **kwargs
    ):
        form = super().get_form(request, obj, **kwargs)

        # Hide certain fields if the user is not superuser
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_superuser'].widget = forms.HiddenInput()

            form.base_fields['password'].disabled = True
            form.base_fields['password'].widget = forms.HiddenInput()

            form.base_fields['groups'].disabled = True
            form.base_fields['groups'].widget = forms.HiddenInput()

            form.base_fields['user_permissions'].disabled = True
            form.base_fields['user_permissions'].widget = forms.HiddenInput()

            form.base_fields['is_staff'].disabled = True
            form.base_fields['is_staff'].widget = forms.HiddenInput()
        return form


admin.site.unregister(UserModel)
admin.site.register(UserModel, UserModelAdmin)
