from django import forms

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
