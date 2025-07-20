from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.template.base import kwarg_re
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView

from products.models import ProductModel
from reviews.forms import AddReviewForm
from reviews.models import ReviewModel


class ReviewAddView(LoginRequiredMixin, CreateView):
    form_class = AddReviewForm
    success_url = reverse_lazy('product-details')
    template_name = 'review.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(ProductModel, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.product = self.product
        review.account = self.request.user
        review.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        return reverse('product-details', kwargs={'id': self.product.pk})


class DeleteReviewView(DeleteView):
    model = ReviewModel

    def get_success_url(self):
        return reverse('product-details', kwargs={'id': self.object.product.id})

    def get_queryset(self):
        return super().get_queryset().filter(account=self.request.user)