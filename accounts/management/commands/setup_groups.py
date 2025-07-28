from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reviews.models import ReviewModel
from products.models import ProductModel
from orders.models import OrderModel

UserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Groups
        review_manager, _ = Group.objects.get_or_create(name='Review Manager')
        product_manager, _ = Group.objects.get_or_create(name='Product Manager')
        orders_manager, _ = Group.objects.get_or_create(name='Orders Manager')
        accounts_manager, _ = Group.objects.get_or_create(name='Accounts Manager')

        # Review Manager - full perms on reviews
        review_ct = ContentType.objects.get_for_model(ReviewModel)
        review_manager.permissions.set(Permission.objects.filter(content_type=review_ct))

        # Product Manager - full perms on products
        product_ct = ContentType.objects.get_for_model(ProductModel)
        product_manager.permissions.set(Permission.objects.filter(content_type=product_ct))

        # Orders Manager - only change permission
        order_ct = ContentType.objects.get_for_model(OrderModel)
        change_order = Permission.objects.get(content_type=order_ct, codename='change_ordermodel')
        orders_manager.permissions.set([change_order])

        # Accounts Manager - change/delete permissions
        account_ct = ContentType.objects.get_for_model(UserModel)
        model_name = UserModel._meta.model_name
        perms = Permission.objects.filter(content_type=account_ct,
                                          codename__in=[f'change_{model_name}', f'delete_{model_name}'])
        accounts_manager.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up.'))
