"""
App configuration for carwash
"""
from django.apps import AppConfig


class CarwashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carwash'
    verbose_name = 'Smart Car Wash & Parking System'

    def ready(self):
        """Customize admin site when app is ready"""
        from django.contrib import admin
        admin.site.site_header = "🚗 Chism Car Care Administration"
        admin.site.site_title = "Chism Car Care"
        admin.site.index_title = "Welcome to Chism Car Care Management System"
