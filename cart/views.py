from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from cart.models import CartModel



class CartDetailsView(LoginRequiredMixin, ListView):
    model = CartModel
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartModel.objects.filter(account_id=self.request.user)