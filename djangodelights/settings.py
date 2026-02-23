from Django_Capstone_project.settings import *  # noqa: F401,F403

# Override settings for the djangodelights package used on PythonAnywhere.
ROOT_URLCONF = "djangodelights.urls"
WSGI_APPLICATION = "djangodelights.wsgi.application"
