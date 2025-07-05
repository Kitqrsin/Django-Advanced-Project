from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import ChamillionUserCreationForm


class RegisterView(CreateView):
    form_class = ChamillionUserCreationForm
    template_name = 'registration/register-profile.html'
    success_url = reverse_lazy('home-page')