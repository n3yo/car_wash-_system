"""
Django Admin configuration for Smart Car Wash System
"""
from django.contrib import admin
from .models import (
    Attendant, Customer, Vehicle, ServiceType,
    ServiceRequest, Parking, Payment
)


@admin.register(Attendant)
class AttendantAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'id_number', 'hire_date', 'is_active']
    list_filter = ['is_active', 'hire_date']
    search_fields = ['name', 'phone', 'email', 'id_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'phone', 'email', 'id_number')
        }),
        ('Employment', {
            'fields': ('hire_date', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'id_number', 'date_registered', 'is_active']
    list_filter = ['is_active', 'date_registered']
    search_fields = ['name', 'phone', 'email', 'id_number']
    readonly_fields = ['date_registered', 'created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'phone', 'email', 'id_number', 'address')
        }),
        ('Account', {
            'fields': ('date_registered', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'customer', 'make', 'model', 'year', 'vehicle_type', 'is_active']
    list_filter = ['vehicle_type', 'color', 'is_active', 'year']
    search_fields = ['plate_number', 'customer__name', 'make', 'model', 'vin']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Vehicle Identification', {
            'fields': ('plate_number', 'vin', 'customer')
        }),
        ('Vehicle Details', {
            'fields': ('make', 'model', 'year', 'vehicle_type', 'color')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'estimated_time_minutes', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description')
        }),
        ('Pricing & Time', {
            'fields': ('base_price', 'estimated_time_minutes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'customer', 'service_type', 'status', 'attendant', 'request_date']
    list_filter = ['status', 'request_date', 'service_type']
    search_fields = ['vehicle__plate_number', 'customer__name']
    readonly_fields = ['request_date', 'created_at', 'updated_at']
    fieldsets = (
        ('Vehicle & Customer', {
            'fields': ('vehicle', 'customer')
        }),
        ('Service Details', {
            'fields': ('service_type', 'attendant', 'notes')
        }),
        ('Timeline', {
            'fields': ('request_date', 'start_time', 'completion_time')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'customer', 'check_in_time', 'check_out_time', 'status', 'parking_fee', 'attendant']
    list_filter = ['status', 'check_in_time']
    search_fields = ['vehicle__plate_number', 'customer__name']
    readonly_fields = ['check_in_time', 'created_at', 'updated_at']
    fieldsets = (
        ('Vehicle & Customer', {
            'fields': ('vehicle', 'customer', 'attendant')
        }),
        ('Parking Timeline', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Fee', {
            'fields': ('parking_fee', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'payment_method', 'status', 'payment_date', 'transaction_ref']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['customer__name', 'transaction_ref']
    readonly_fields = ['payment_date', 'created_at', 'updated_at']
    fieldsets = (
        ('Customer & Amount', {
            'fields': ('customer', 'amount', 'payment_method')
        }),
        ('Related Records', {
            'fields': ('service_request', 'parking')
        }),
        ('Payment Details', {
            'fields': ('status', 'transaction_ref', 'payment_date', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
