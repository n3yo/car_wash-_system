"""
Models for Smart Car Wash & Parking System
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Attendant(models.Model):
    """Employee/Attendant who receives and processes vehicles"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    id_number = models.CharField(max_length=50, unique=True)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Attendants"

    def __str__(self):
        return f"{self.name} ({self.id_number})"


class Customer(models.Model):
    """Customer/Vehicle Owner"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    id_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    date_registered = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Vehicle(models.Model):
    """Vehicle Information"""
    VEHICLE_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('hatchback', 'Hatchback'),
        ('pickup', 'Pickup'),
        ('other', 'Other'),
    ]

    COLORS = [
        ('white', 'White'),
        ('black', 'Black'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('silver', 'Silver'),
        ('gray', 'Gray'),
        ('other', 'Other'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    color = models.CharField(max_length=20, choices=COLORS)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vin = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plate_number']
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.plate_number} - {self.make} {self.model} ({self.year})"


class ServiceType(models.Model):
    """Available Car Wash Services"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_time_minutes = models.IntegerField(help_text="Estimated service duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Service Types"

    def __str__(self):
        return f"{self.name} (TZS {self.base_price})"


class ServiceRequest(models.Model):
    """Service Request for a Vehicle"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_requests')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='service_requests')
    attendant = models.ForeignKey(Attendant, on_delete=models.SET_NULL, null=True, related_name='service_requests')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name='requests')
    request_date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    completion_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-request_date']
        verbose_name_plural = "Service Requests"

    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.service_type.name} ({self.status})"


class Parking(models.Model):
    """Parking Records"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='parking_records')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='parking_records')
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    parking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    attendant = models.ForeignKey(Attendant, on_delete=models.SET_NULL, null=True, related_name='parking_records')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-check_in_time']
        verbose_name_plural = "Parking Records"

    def __str__(self):
        return f"{self.vehicle.plate_number} - Parked at {self.check_in_time}"


class Payment(models.Model):
    """Payment Records"""
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'Mobile Money'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    parking = models.OneToOneField(Parking, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_ref = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment of TZS {self.amount} - {self.status}"
