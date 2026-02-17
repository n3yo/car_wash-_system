"""
DRF Serializers for Smart Car Wash System
"""
from rest_framework import serializers
from .models import (
    Attendant, Customer, Vehicle, ServiceType,
    ServiceRequest, Parking, Payment
)


class AttendantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendant
        fields = [
            'id', 'name', 'phone', 'email', 'id_number',
            'hire_date', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'email', 'id_number',
            'address', 'date_registered', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['date_registered', 'created_at', 'updated_at']


class VehicleSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'customer', 'customer_name', 'plate_number',
            'vehicle_type', 'color', 'make', 'model', 'year',
            'vin', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = [
            'id', 'name', 'description', 'base_price',
            'estimated_time_minutes', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ServiceRequestSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    attendant_name = serializers.CharField(source='attendant.name', read_only=True)
    service_name = serializers.CharField(source='service_type.name', read_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'vehicle', 'vehicle_plate', 'customer', 'customer_name',
            'attendant', 'attendant_name', 'service_type', 'service_name',
            'request_date', 'start_time', 'completion_time', 'status',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['request_date', 'created_at', 'updated_at']


class ParkingSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.plate_number', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    attendant_name = serializers.CharField(source='attendant.name', read_only=True)

    class Meta:
        model = Parking
        fields = [
            'id', 'vehicle', 'vehicle_plate', 'customer', 'customer_name',
            'check_in_time', 'check_out_time', 'status', 'parking_fee',
            'attendant', 'attendant_name', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['check_in_time', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    service_detail = ServiceRequestSerializer(source='service_request', read_only=True)
    parking_detail = ParkingSerializer(source='parking', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'customer', 'customer_name', 'service_request',
            'service_detail', 'parking', 'parking_detail',
            'amount', 'payment_method', 'status', 'transaction_ref',
            'payment_date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['payment_date', 'created_at', 'updated_at']
