from django.contrib import admin

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
	list_display = ("name", "quantity", "unit_price")
	search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ("name", "price")
	search_fields = ("name",)


@admin.register(RecipeRequirement)
class RecipeRequirementAdmin(admin.ModelAdmin):
	list_display = ("menu_item", "ingredient", "quantity")
	list_filter = ("menu_item", "ingredient")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
	list_display = ("menu_item", "timestamp")
	list_filter = ("timestamp",)
