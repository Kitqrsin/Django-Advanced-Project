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
    size_name = request.POST.get('size_name')
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        product = ProductModel.objects.get(id=product_id)
        cart, _ = CartModel.objects.get_or_create(account=request.user)
        product_size = product.productsize_set.filter(size__size_name=size_name).first()
        if not product_size:
            return JsonResponse({'success': False, 'error': 'Invalid size'})
        cart_product, created = CartsProductsModel.objects.get_or_create(
            carts=cart, products=product, size=product_size.size,
            defaults={'quantity': quantity}
        )
        if not created:
            if (cart_product.quantity + quantity) > product_size.quantity:
                return JsonResponse({'success': False, 'error': 'Too much quantity selected (check existing in cart)'})

            cart_product.quantity += quantity
            cart_product.save()
        return JsonResponse({'success': True})

    # if user is anonymous
    else:
        cart = get_cart(request)
        key = f"{product_id}|{size_name}"

        # Validations for cart:
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})

        product_size = product.productsize_set.filter(size__size_name=size_name).first()
        if not product_size:
            return JsonResponse({'success': False, 'error': 'Invalid size'})

        current_qty = cart.get(key, 0)
        if current_qty + quantity > product_size.quantity:
            return JsonResponse({'success': False, 'error': 'Too much quantity selected (check existing in cart)'})

        cart[key] = cart.get(key, 0) + quantity
        request.session.modified = True
        return JsonResponse({'success': True})

@require_POST
def subtract_from_cart(request):
    size_name = request.POST.get('size_name')
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        try:
            cart = CartModel.objects.get(account=request.user)

            product = ProductModel.objects.get(id=product_id)
            product_size = product.productsize_set.filter(size__size_name=size_name).first()
            cart_product = CartsProductsModel.objects.get(carts=cart, products_id=product_id, size=product_size.size)
            max_qty = product_size.quantity if product_size else 0
            if cart_product:
                if quantity == 0:
                    cart_product.delete()
                else:
                    if quantity > max_qty:
                        messages.error(request, f'The maximum amount possible is: {max_qty}')
                    else:
                        cart_product.quantity = quantity
                        cart_product.save()
            return HttpResponseRedirect(reverse('cart'))
        except (CartModel.DoesNotExist, CartsProductsModel.DoesNotExist, ProductModel.DoesNotExist):
            pass

    else:
        cart = request.session.get('cart', {})
        key = f"{product_id}|{size_name}"
        product = ProductModel.objects.get(id=product_id)
        product_size = product.productsize_set.filter(size__size_name=size_name).first()
        max_qty = product_size.quantity if product_size else 0
        if key in cart:
            if quantity == 0:
                del cart[key]
            else:
                if quantity > max_qty:
                    messages.error(request, f'The maximum amount possible is: {max_qty}')

                else:
                    cart[key] = quantity
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
            # since the key for anonymous cart resembles: "3|M"
            products = ProductModel.objects.filter(id__in=[key.split('|')[0] for key in cart.keys()])
            cart_items = []

            for key, qty in cart.items():
                product_id, size_name = key.split("|")
                product = next((p for p in products if str(p.id) == product_id), None)
                if product:
                    # Create a new class CartItem and instance of it with attributes products, size_name and quantity
                    # then append it to the cart_items list
                    cart_items.append(type('CartItem', (), {
                        'products': product,
                        'size_name': size_name,
                        'quantity': qty,
                    })())
            return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        total = sum(item.quantity * item.products.unit_price for item in cart_items)
        context['total'] = total
        return context
