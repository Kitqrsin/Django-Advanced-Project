from django.shortcuts import render
from django.views.generic import ListView

from products.models import ProductModel


# Create your views here.
def search_result(request):
    query = request.GET.get('query', '')
    products = ProductModel.objects.filter(product_name__icontains=query) if query else []
    context = {
        'query': query,
        'products': products
    }

    return render(request,
                  'search.html',
                  context=context)


class HomePage(ListView):
    model = ProductModel
    template_name = 'home_page.html'
    context_object_name = 'products'
