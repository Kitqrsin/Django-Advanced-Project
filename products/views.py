from django.shortcuts import render
from django.views.generic import DetailView

from products.models import ProductModel


# Create your views here.
class ProductDetailsView(DetailView):
    template_name = 'product-details.html'
    model = ProductModel
    pk_url_kwarg = 'id'
    context_object_name = 'current_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_product = self.get_object()
        size_data = {
            ps.size.size_name: ps.quantity
            for ps in current_product.productsize_set.all()
        }
        context['size_data'] = size_data
        context['all_sizes'] = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        context['reviews'] = self.object.product_reviews.all()
        return context