from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from cart.models import CartModel, CartsProductsModel
from products.models import ProductModel


@receiver(user_logged_in)
def merge_session_cart_to_user_cart(sender, user, request, **kwargs):
    session_cart = request.session.get('cart', {})

    if session_cart:
        cart, _ = CartModel.objects.get_or_create(account=user)
        for product_id, quantity in session_cart.items():
            try:
                product = ProductModel.objects.get(id=product_id)
                cart_product, created = CartsProductsModel.objects.get_or_create(
                    carts=cart, products=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_product.quantity += quantity
                    cart_product.save()
            except ProductModel.DoesNotExist:
                continue

        request.session['cart'] = {}
        request.session.modified = True