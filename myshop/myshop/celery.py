"""adds Celery to the project

What this does:

Sets the DJANGO_SETTINGS_MODULE variable for the Celery command-line program.

Creates an instance of the application.

Loads any custom configuration from the project settings. Namespace specifies the prefix
that Celery-related settings will have in the settings.py file. By setting the CELERY
namespace, all Celery settings need to include the CELERY_ prefix in their name.

Tells Celery to auto-discover asynchronous tasks for the applications. Celery will look
for a tasks.py file in each application directory of apps added to INSTALLED_APPS in
order to load async tasks defined in it.
"""

import logging.config
import os

from celery import Celery
from django.conf import settings

logger = logging.getLogger("payment")

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")

# create an instance of the application
app = Celery("myshop")
# load any custom configuration from project settings
app.config_from_object("django.conf:settings", namespace="CELERY")
# have Celery autodiscover asynchronous tasks for the apps
app.autodiscover_tasks()

# Configure Celery logging to use Django's logging settings
logging.config.dictConfig(settings.LOGGING)
