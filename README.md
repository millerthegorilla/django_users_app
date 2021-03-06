# Django_Users_App

Django_users_app is a Django app to add user functionality to your project.

Detailed documentation is in the "docs" directory.  Eventually.

The packages :
 'django-email-verification' (https://pypi.org/project/django-email-verification/) 
 and...
  'django-recaptcha' (https://pypi.org/project/django-recaptcha/) 

are required dependencies.

## Installation

You can install this package from source....   don't forget to use either a virtualenv or a container.

## Quick Start


1. Add "django_users_app", as well as the dependencies, to your INSTALLED_APPS setting like this::
```
INSTALLED_APPS = [
    ...
    'django_users_app',
    'django_email_validation',
    'captcha'
]
```
2. Add the django_user_app middleware to your project to force a superuser to reauthenticate if they access the admin panel after being logged in as a user.
```
MIDDLEWARE = [
    ...
    'django_users_app.middleware.ReauthenticateMiddleware',
]
```
 3. Include the users URLconf in your project urls.py like this::

  path('users/', include('django_users_app.urls')),

4. Run ``python manage.py migrate`` to create the users models.

5. Start the development server and visit http://127.0.0.1:8000/admin/    to create a user (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/users/accounts/login to register/login.

You can incorporate the tests in your project by defining a file 'tests.py' in your project directory, and including the following line in that file...
```from django_users_app.tests import *```
