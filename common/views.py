from django.shortcuts import render
from django.views.generic import ListView

from products.models import ProductModel


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

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(categories=category_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryModel.objects.all()
        context['selected_category'] = self.request.GET.get('category', None)
        return context

