from django.contrib.auth import get_user_model, update_session_auth_hash
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from accounts.forms import ChamillionUserCreationForm, ChamillionUserEditForm
from accounts.mixins import CheckUserMixin

UserModel = get_user_model()

class RegisterView(CreateView):
    form_class = ChamillionUserCreationForm
    template_name = 'registration/register-profile.html'
    success_url = reverse_lazy('login-user')

class AccountDetailsView(CheckUserMixin, DetailView):
    template_name = 'profile-details.html'
    model = UserModel
    context_object_name = 'user_profile'
    pk_url_kwarg = 'id'


class AccountEditView(CheckUserMixin, UpdateView):
    form_class = ChamillionUserEditForm
    template_name = 'profile-edit.html'
    pk_url_kwarg = 'id'
    model = UserModel

    def get_success_url(self):
        return reverse('user-details', kwargs={'id': self.object.id})

    # change password logic
    def form_valid(self, form):
        response = super().form_valid(form)
        new_password = self.request.POST.get('change-password')
        confirm_password = self.request.POST.get('confirm-change-password')


        if new_password == "":
            pass

        elif confirm_password == new_password and new_password:
            self.object.set_password(new_password)
            self.object.save()

            # to keep the user logged in after change
            update_session_auth_hash(self.request, self.object)
        else:
            form.add_error(None, "Invalid password confirmation! Please make sure both fields are the same")
            return self.form_invalid(form)
        return response


class AccountDeleteView(CheckUserMixin, DeleteView):
    model = UserModel
    success_url = reverse_lazy('home-page')
    pk_url_kwarg = 'id'


