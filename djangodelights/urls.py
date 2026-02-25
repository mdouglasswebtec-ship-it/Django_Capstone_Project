"""
URL configuration for djangodelights project.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from inventory.forms import UsernameOrEmailAuthenticationForm
from inventory.views import signup

urlpatterns = [
	path("admin/", admin.site.urls),
	path(
		"accounts/login/",
		auth_views.LoginView.as_view(
			template_name="registration/login.html",
			authentication_form=UsernameOrEmailAuthenticationForm,
		),
		name="login",
	),
	path("accounts/logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
	path("accounts/signup/", signup, name="signup"),
	path("", include("inventory.urls")),
]
