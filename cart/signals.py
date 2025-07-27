from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from cart.models import CartModel, CartsProductsModel
from products.models import ProductModel

"""
    Removed due to complications with user abusing the max quantity of products which exceeds the set amount from
    the database
"""


# if anonymous user has a session cart with products in it and logs in a profile with already
# existing cart: add the items from the session to the cart of the account and remove the session

# @receiver(user_logged_in)
# def merge_session_cart_to_user_cart(sender, user, request, **kwargs):
#     session_cart = request.session.get('cart', {})
#
#     if session_cart:
#         cart, _ = CartModel.objects.get_or_create(account=user)
#         for product_id, quantity in session_cart.items():
#             try:
#                 product = ProductModel.objects.get(id=product_id)
#                 cart_product, created = CartsProductsModel.objects.get_or_create(
#                     carts=cart, products=product,
#                     defaults={'quantity': quantity}
#                 )
#                 if not created:
#                     cart_product.quantity += quantity
#                     cart_product.save()
#             except ProductModel.DoesNotExist:
#                 continue
#
#         request.session['cart'] = {}
#         request.session.modified = True