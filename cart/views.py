from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from cart.models import CartModel, CartsProductsModel
from products.models import ProductModel


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = CartModel.objects.get_or_create(account=request.user)
        return cart
    else:
        return request.session.setdefault('cart', {})

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        product = ProductModel.objects.get(id=product_id)
        cart, _ = CartModel.objects.get_or_create(account=request.user)
        cart_product, created = CartsProductsModel.objects.get_or_create(
            carts=cart, products=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        return JsonResponse({'success': True})
    else:
        cart = get_cart(request)
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session.modified = True
        return JsonResponse({'success': True})

@require_POST
def subtract_from_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        try:
            cart = CartModel.objects.get(account=request.user)
            cart_product = CartsProductsModel.objects.get(carts=cart, products_id=product_id)
            product_quantity_available = ProductModel.objects.get(id=product_id)
            if cart_product:
                if quantity == 0:
                    cart_product.delete()
                else:
                    if quantity > product_quantity_available.quantity:
                        messages.error(request, f'The maximum amount possible is: {product_quantity_available.quantity}')
                    else:
                        cart_product.quantity = quantity
                        cart_product.save()
            return HttpResponseRedirect(reverse('cart'))
        except (CartModel.DoesNotExist, CartsProductsModel.DoesNotExist, ProductModel.DoesNotExist):
            pass

    else:
        cart = request.session.get('cart', {})
        product_quantity_available = ProductModel.objects.get(id=product_id)
        if product_id in cart:
            if quantity == 0:
                del cart[product_id]
            else:
                if quantity > product_quantity_available.quantity:
                    messages.error(request, f'The maximum amount possible is: {product_quantity_available.quantity}')

                else:
                    cart[product_id] = quantity
            request.session['cart'] = cart
            request.session.modified = True

    return redirect('cart')

class CartDetailsView(ListView):
    model = CartsProductsModel
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            try:
                cart = CartModel.objects.get(account=self.request.user)
                return CartsProductsModel.objects.filter(carts=cart).select_related('products')
            except CartModel.DoesNotExist:
                return []
        else:
            cart = self.request.session.get('cart', {})
            products = ProductModel.objects.filter(id__in=cart.keys())
            cart_items = []
            for product in products:
                cart_items.append(type('CartItem', (), {
                    'products': product,
                    'quantity': cart[str(product.id)],
                })())
            return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        total = sum(item.quantity * item.products.unit_price for item in cart_items)
        context['total'] = total
        return context
