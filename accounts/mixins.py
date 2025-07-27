from django.core.exceptions import PermissionDenied

# Checks if the current user is the same user trying to edit/delete an account
class CheckUserMixin:
    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user.id != obj.id:
            raise PermissionDenied
        return obj
