from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ingredients/", views.ingredient_list, name="ingredient_list"),
    path("ingredients/add/", views.ingredient_create, name="ingredient_create"),
    path("ingredients/<int:ingredient_id>/edit/", views.ingredient_update, name="ingredient_update"),
    path("ingredients/<int:ingredient_id>/delete/", views.ingredient_delete, name="ingredient_delete"),
    path("menu/", views.menu_list, name="menu_list"),
    path("menu/add/", views.menu_item_create, name="menu_item_create"),
    path("recipes/add/", views.recipe_requirement_create, name="recipe_requirement_create"),
    path("purchases/", views.purchase_list, name="purchase_list"),
    path("purchases/add/", views.purchase_create, name="purchase_create"),
    path("report/", views.report, name="report"),
    path("restock/", views.restock_report, name="restock_report"),
]
