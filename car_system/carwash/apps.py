"""
App configuration for carwash
"""
from django.apps import AppConfig


class CarwashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carwash'
    verbose_name = 'Smart Car Wash & Parking System'
