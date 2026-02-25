"""
Create the default superuser if it does not already exist.

Usage:
    python manage.py setup_admin
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the default admin superuser (Mathew) if it does not exist."

    def handle(self, *args, **options):
        User = get_user_model()
        username = "Mathew"
        email = "mdouglasswebtec@gmail.com"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Superuser '{}' already exists.".format(username)))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password="Mathew06!",
            )
            self.stdout.write(self.style.SUCCESS("Superuser '{}' created successfully.".format(username)))
