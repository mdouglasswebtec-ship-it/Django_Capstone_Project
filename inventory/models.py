from django.db import models


class Ingredient(models.Model):
	name = models.CharField(max_length=100, unique=True)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self) -> str:
		return f"{self.name}"


class MenuItem(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self) -> str:
		return f"{self.name}"


class RecipeRequirement(models.Model):
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="recipe_requirements")
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="recipe_requirements")
	quantity = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self) -> str:
		return f"{self.quantity} {self.ingredient.name} for {self.menu_item.name}"


class Purchase(models.Model):
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="purchases")
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.menu_item.name} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
