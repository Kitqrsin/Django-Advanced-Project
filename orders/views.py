import requests
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from products.models import ProductModel
from orders.forms import OrderForm
from orders.models import OrderItemsModel

ECONT_API_URL = "https://demo.econt.com/ee/services/Nomenclatures/NomenclaturesService.getOffices.json"
ECONT_API_USER = "iasp-dev"
ECONT_API_PASS = "1Asp-dev"


def econt_offices_api(request):
    offices = get_econt_offices()

    valid_offices = [
        {
            "name": office.get("name"),
            "address": office.get("address"),
            "latitude": office.get("latitude"),
            "longitude": office.get("longitude"),
        }
        for office in offices
        if office.get("latitude") is not None and office.get("longitude") is not None
    ]
    return JsonResponse(valid_offices, safe=False)


def get_econt_offices():
    payload = {
        "client": {
            "username": ECONT_API_USER,
            "password": ECONT_API_PASS
        }
    }

    try:
        response = requests.post(ECONT_API_URL, json=payload)
        response.raise_for_status()
        all_offices = response.json().get("offices", [])
    except requests.RequestException:
        return []

    bg_offices = [
        office for office in all_offices
        if office.get("address", {}).get("city", {}).get("country", {}).get("code2") == "BG"
    ]
    simplified = []
    for office in bg_offices:
        loc = office.get("address", {}).get("location", {})
        simplified.append({
            "code": office.get("id"),
            "name": office.get("name"),
            "address": office.get("address", {}).get("fullAddress"),
            "latitude": loc.get("latitude"),
            "longitude": loc.get("longitude"),
        })
    return simplified

class CheckoutView(FormView):
    template_name = 'checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('home-page')

    # get_initial is used to fill out the form from the view with the information from the cart/account
    # also handles cases where the user is anonymous
    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        if user.is_authenticated:
            cart = getattr(user, 'cart', None)
            total_price = 0
            for cart_item in cart.cart_products.all():
                total_price += cart_item.quantity * cart_item.products.unit_price
            initial.update({
                'total_price': total_price,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': getattr(user, 'phone_number', ''),
            })

        else:
            session_cart = self.request.session.get('cart', {})
            total_price = 0
            for product_id, quantity in session_cart.items():
                try:
                    product = ProductModel.objects.get(id=product_id)
                    total_price += product.unit_price * quantity
                except ProductModel.DoesNotExist:
                    continue

            initial.update({
                'total_price': total_price,
                'first_name': '',
                'last_name': '',
                'email': '',
                'phone': '',
            })

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.get_initial().get('total_price', 0)
        return context

    def form_valid(self, form):
        user = self.request.user
        total_price = 0

        # for logged in users
        if user.is_authenticated:
            cart = getattr(user, 'cart', None)

            for cart_item in cart.cart_products.all():
                total_price += cart_item.quantity * cart_item.products.unit_price

            order = form.save(commit=False)
            order.account = user
            order.total_price = total_price
            order.first_name = user.first_name
            order.last_name = user.last_name
            order.email = user.email
            order.phone = user.phone_number
            order.save()

            for cart_item in cart.cart_products.all():
                OrderItemsModel.objects.create(
                    orders=order,
                    items=cart_item.products,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.products.unit_price
                )

            cart.cart_products.all().delete()

        # for anonymous users
        else:
            cart = self.request.session.get('cart', {})

            for product_id, quantity in cart.items():
                product = ProductModel.objects.get(id=product_id)
                total_price += product.unit_price * quantity

            order = form.save(commit=False)
            order.account = None
            order.total_price = total_price
            order.save()

            for product_id, quantity in cart.items():
                try:
                    product = ProductModel.objects.get(id=product_id)
                    OrderItemsModel.objects.create(
                        orders=order,
                        items=product,
                        quantity=quantity,
                        unit_price=product.unit_price
                    )
                except ProductModel.DoesNotExist:
                    continue

            self.request.session['cart'] = {}
            self.request.session.modified = True

        return super().form_valid(form)
