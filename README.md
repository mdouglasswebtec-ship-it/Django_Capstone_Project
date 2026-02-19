# Django-Capstone-Project

## Wireframe

```
Header: Django Delights | Home | Inventory | Menu | Purchases | Report | Restock | Login/Logout

Home
	- Welcome card

Inventory
	- Table: Ingredient | Quantity | Unit Price | Actions (Edit/Delete)
	- Button: Add Ingredient

Menu
	- Card list: Menu Item + Price
	- Recipe Requirements list
	- Buttons: Add Menu Item, Add Recipe Requirement

Purchases
	- Table: Menu Item | Price | Timestamp
	- Button: Record Purchase

Report
	- Total Revenue / Total Cost / Profit

Restock
	- Table: Ingredient | Required | In Stock | Shortfall
```

## Example Queries

Run these in the Django shell:

```
/workspaces/Django-Capstone-Project/.venv/bin/python manage.py shell
```

```python
from django.db.models import F, Sum
from inventory.models import Ingredient, MenuItem, Purchase, RecipeRequirement

# Inventory list
Ingredient.objects.all().order_by("name")

# Purchases log
Purchase.objects.select_related("menu_item").order_by("-timestamp")

# Menu with ingredients
MenuItem.objects.prefetch_related("recipe_requirements__ingredient")

# Total revenue
Purchase.objects.aggregate(total=Sum("menu_item__price"))

# Total cost (sum of all ingredients used in all purchases)
Purchase.objects.aggregate(
	total=Sum(
		F("menu_item__recipe_requirements__quantity")
		* F("menu_item__recipe_requirements__ingredient__unit_price")
	)
)

# Profit (revenue - cost)
revenue = Purchase.objects.aggregate(total=Sum("menu_item__price"))["total"] or 0
cost = Purchase.objects.aggregate(
	total=Sum(
		F("menu_item__recipe_requirements__quantity")
		* F("menu_item__recipe_requirements__ingredient__unit_price")
	)
)["total"] or 0
profit = revenue - cost
profit
```

## Git Setup and Commits

Initialize and push your repository:

```
git init
git add .
git commit -m "Initialize Django Delights project"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

Commit regularly as you work:

```
git status
git add <files>
git commit -m "Add inventory models and migrations"
```