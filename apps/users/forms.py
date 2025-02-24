from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username")
