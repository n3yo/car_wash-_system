"""
URL configuration for carwash app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'attendants', views.AttendantViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'services', views.ServiceTypeViewSet)
router.register(r'service-requests', views.ServiceRequestViewSet)
router.register(r'parking', views.ParkingViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
