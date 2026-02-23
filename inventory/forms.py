from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db.utils import OperationalError, ProgrammingError

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "quantity", "unit_price"]


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "price"]


class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ["menu_item", "ingredient", "quantity"]


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["menu_item"]


class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["quantity", "unit_price"]


class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            user_model = get_user_model()
            lookup_username = username_or_email
            if "@" in username_or_email:
                try:
                    lookup_username = user_model.objects.get(
                        email__iexact=username_or_email
                    ).get_username()
                except user_model.DoesNotExist:
                    lookup_username = username_or_email

            try:
                self.user_cache = authenticate(
                    self.request, username=lookup_username, password=password
                )
            except (OperationalError, ProgrammingError):
                raise self.get_invalid_login_error()
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
