"""
URL configuration for djangodelights project.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from inventory.forms import UsernameOrEmailAuthenticationForm

urlpatterns = [
	path("admin/", admin.site.urls),
	# Keep auth routes explicit and simple for hosted environments.
	# Use Django's default auth template path: registration/login.html
	path(
		"accounts/login/",
		auth_views.LoginView.as_view(
			template_name="admin/login.html",
			authentication_form=UsernameOrEmailAuthenticationForm,
		),
		name="login",
	),
	path("accounts/logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
	path("", include("inventory.urls")),
]
