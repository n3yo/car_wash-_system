"""
Unit tests for Smart Car Wash System
"""
from django.test import TestCase
from django.utils import timezone
from .models import (
    Attendant, Customer, Vehicle, ServiceType,
    ServiceRequest, Parking, Payment
)


class AttendantModelTest(TestCase):
    def setUp(self):
        self.attendant = Attendant.objects.create(
            name="John Doe",
            phone="+255123456789",
            email="john@example.com",
            id_number="ID123456"
        )

    def test_attendant_creation(self):
        self.assertTrue(self.attendant.is_active)
        self.assertEqual(self.attendant.name, "John Doe")

    def test_attendant_string_representation(self):
        self.assertEqual(str(self.attendant), "John Doe (ID123456)")


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Jane Smith",
            phone="+255987654321",
            email="jane@example.com",
            id_number="ID654321",
            address="Dar es Salaam, Tanzania"
        )

    def test_customer_creation(self):
        self.assertTrue(self.customer.is_active)
        self.assertEqual(self.customer.name, "Jane Smith")

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), "Jane Smith (+255987654321)")


class VehicleModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Jane Smith",
            phone="+255987654321",
            email="jane@example.com",
            id_number="ID654321",
            address="Dar es Salaam"
        )
        self.vehicle = Vehicle.objects.create(
            customer=self.customer,
            plate_number="TZA-1234-AB",
            vehicle_type="sedan",
            color="black",
            make="Toyota",
            model="Camry",
            year=2020
        )

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.plate_number, "TZA-1234-AB")
        self.assertEqual(self.vehicle.make, "Toyota")

    def test_vehicle_string_representation(self):
        expected = "TZA-1234-AB - Toyota Camry (2020)"
        self.assertEqual(str(self.vehicle), expected)
