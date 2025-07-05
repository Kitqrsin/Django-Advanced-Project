from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()

class ChamillionUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''