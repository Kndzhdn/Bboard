from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Доска объявлений'









from django.dispatch import Signal
from .utilities import send_activation_notification

user_registered = Signal(providing_args=['instance'])

def user_registered_dispatcher(sender, **kwargs):
	send_activation_notification(kwargs['instance'])

user_registered.connect(user_registered_dispatcher)
