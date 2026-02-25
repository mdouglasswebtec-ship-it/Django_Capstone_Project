from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
	IngredientForm,
	IngredientUpdateForm,
	MenuItemForm,
	PurchaseForm,
	RecipeRequirementForm,
)
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


def signup(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Account created! Welcome to Django Delights.")
			return redirect("home")
	else:
		form = UserCreationForm()
	return render(request, "registration/signup.html", {"form": form})


def home(request):
	return render(request, "index.html")


def ingredient_list(request):
	ingredients = Ingredient.objects.all().order_by("name")
	return render(request, "inventory/ingredient_list.html", {"ingredients": ingredients})


def menu_list(request):
	menu_items = MenuItem.objects.prefetch_related("recipe_requirements__ingredient").order_by("name")
	return render(request, "inventory/menu_list.html", {"menu_items": menu_items})


def purchase_list(request):
	purchases = Purchase.objects.select_related("menu_item").order_by("-timestamp")
	return render(request, "inventory/purchase_list.html", {"purchases": purchases})


def report(request):
	purchases = Purchase.objects.select_related("menu_item").prefetch_related(
		"menu_item__recipe_requirements__ingredient"
	)

	total_revenue = Decimal("0.00")
	total_cost = Decimal("0.00")

	for purchase in purchases:
		total_revenue += purchase.menu_item.price
		for requirement in purchase.menu_item.recipe_requirements.all():
			total_cost += requirement.quantity * requirement.ingredient.unit_price

	profit = total_revenue - total_cost

	context = {
		"total_revenue": total_revenue,
		"total_cost": total_cost,
		"profit": profit,
	}
	return render(request, "inventory/report.html", context)


def restock_report(request):
	requirements = RecipeRequirement.objects.select_related("ingredient")
	required_totals = {}

	for requirement in requirements:
		ingredient_id = requirement.ingredient_id
		required_totals[ingredient_id] = required_totals.get(ingredient_id, Decimal("0.00")) + requirement.quantity

	restock_rows = []
	for ingredient in Ingredient.objects.all().order_by("name"):
		required = required_totals.get(ingredient.id, Decimal("0.00"))
		shortfall = required - ingredient.quantity
		if shortfall > 0:
			restock_rows.append(
				{
					"ingredient": ingredient,
					"required": required,
					"shortfall": shortfall,
				}
			)

	return render(request, "inventory/restock_report.html", {"restock_rows": restock_rows})


def ingredient_create(request):
	if request.method == "POST":
		form = IngredientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Ingredient added to inventory.")
			return redirect("ingredient_list")
	else:
		form = IngredientForm()

	return render(request, "inventory/ingredient_form.html", {"form": form, "title": "Add Ingredient"})


def ingredient_update(request, ingredient_id):
	ingredient = get_object_or_404(Ingredient, id=ingredient_id)
	if request.method == "POST":
		form = IngredientUpdateForm(request.POST, instance=ingredient)
		if form.is_valid():
			form.save()
			messages.success(request, "Ingredient updated.")
			return redirect("ingredient_list")
	else:
		form = IngredientUpdateForm(instance=ingredient)

	return render(
		request,
		"inventory/ingredient_form.html",
		{"form": form, "title": f"Update {ingredient.name}"},
	)


def ingredient_delete(request, ingredient_id):
	ingredient = get_object_or_404(Ingredient, id=ingredient_id)
	if request.method == "POST":
		ingredient.delete()
		messages.success(request, "Ingredient deleted.")
	return redirect("ingredient_list")


def menu_item_create(request):
	if request.method == "POST":
		form = MenuItemForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Menu item created.")
			return redirect("menu_list")
	else:
		form = MenuItemForm()

	return render(request, "inventory/menu_item_form.html", {"form": form, "title": "Add Menu Item"})


def recipe_requirement_create(request):
	if request.method == "POST":
		form = RecipeRequirementForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Recipe requirement added.")
			return redirect("menu_list")
	else:
		form = RecipeRequirementForm()

	return render(
		request,
		"inventory/recipe_requirement_form.html",
		{"form": form, "title": "Add Recipe Requirement"},
	)


def purchase_create(request):
	if request.method == "POST":
		form = PurchaseForm(request.POST)
		if form.is_valid():
			menu_item = form.cleaned_data["menu_item"]
			requirements = RecipeRequirement.objects.select_related("ingredient").filter(menu_item=menu_item)

			insufficient = []
			for requirement in requirements:
				if requirement.ingredient.quantity < requirement.quantity:
					insufficient.append(requirement.ingredient.name)

			if insufficient:
				messages.error(
					request,
					"Not enough inventory for: " + ", ".join(insufficient),
				)
			else:
				with transaction.atomic():
					Purchase.objects.create(menu_item=menu_item)
					for requirement in requirements:
						ingredient = requirement.ingredient
						ingredient.quantity -= requirement.quantity
						ingredient.save(update_fields=["quantity"])
				messages.success(request, "Purchase recorded.")
				return redirect("purchase_list")
	else:
		form = PurchaseForm()

	return render(request, "inventory/purchase_form.html", {"form": form, "title": "Record Purchase"})
