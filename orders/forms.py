from django import forms
from .models import OrderModel

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        exclude = ['account', 'created_at', 'status', 'total_price']
        widgets = {
            'delivery_method': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            if user and user.is_authenticated:
                for field_name in []:
                    self.fields[field_name].widget = forms.HiddenInput()
                    self.initial[field_name] = getattr(user, field_name, '')