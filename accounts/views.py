from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import ChamillionUserCreationForm, ChamillionUserEditForm


class RegisterView(CreateView):
    form_class = ChamillionUserCreationForm
    template_name = 'registration/register-profile.html'
    success_url = reverse_lazy('home-page')

class AccountDetailsView(DetailView):
    template_name = 'profile-details.html'
    model = get_user_model()
    context_object_name = 'user_profile'
    pk_url_kwarg = 'id'

class AccountEditView(UpdateView):
    form_class = ChamillionUserEditForm
    template_name = 'profile-edit.html'
    pk_url_kwarg = 'id'
    model = get_user_model()

    def get_success_url(self):
        return reverse('user-details', kwargs={'id': self.object.id})
