"""
Views for Smart Car Wash System API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import (
    Attendant, Customer, Vehicle, ServiceType,
    ServiceRequest, Parking, Payment
)
from .serializers import (
    AttendantSerializer, CustomerSerializer, VehicleSerializer,
    ServiceTypeSerializer, ServiceRequestSerializer,
    ParkingSerializer, PaymentSerializer
)


class AttendantViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Attendants"""
    queryset = Attendant.objects.all()
    serializer_class = AttendantSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get performance statistics for an attendant"""
        attendant = self.get_object()
        services_completed = attendant.service_requests.filter(status='completed').count()
        total_parking_handled = attendant.parking_records.all().count()

        return Response({
            'attendant': AttendantSerializer(attendant).data,
            'services_completed': services_completed,
            'parking_handled': total_parking_handled,
        })


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Customers"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get customer summary and history"""
        customer = self.get_object()
        vehicles_count = customer.vehicles.count()
        total_spent = customer.payments.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0

        recent_services = customer.service_requests.all()[:5]
        recent_parking = customer.parking_records.all()[:5]

        return Response({
            'customer': CustomerSerializer(customer).data,
            'vehicles_count': vehicles_count,
            'total_spent': str(total_spent),
            'recent_services': ServiceRequestSerializer(recent_services, many=True).data,
            'recent_parking': ParkingSerializer(recent_parking, many=True).data,
        })


class VehicleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Vehicles"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        """Filter vehicles by customer if provided"""
        queryset = Vehicle.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        return queryset

    @action(detail=True, methods=['get'])
    def service_history(self, request, pk=None):
        """Get service history for a vehicle"""
        vehicle = self.get_object()
        services = vehicle.service_requests.all()
        return Response({
            'vehicle': VehicleSerializer(vehicle).data,
            'services': ServiceRequestSerializer(services, many=True).data,
        })


class ServiceTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Service Types"""
    queryset = ServiceType.objects.filter(is_active=True)
    serializer_class = ServiceTypeSerializer


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Service Requests"""
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending service requests"""
        pending_services = ServiceRequest.objects.filter(status='pending')
        serializer = self.get_serializer(pending_services, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def start_service(self, request, pk=None):
        """Mark service as in progress"""
        service = self.get_object()
        if service.status != 'pending':
            return Response(
                {'error': 'Only pending services can be started'},
                status=status.HTTP_400_BAD_REQUEST
            )
        service.status = 'in_progress'
        service.start_time = timezone.now()
        if not service.attendant:
            service.attendant = request.user  # Assign current user if available
        service.save()
        return Response(ServiceRequestSerializer(service).data)

    @action(detail=True, methods=['post'])
    def complete_service(self, request, pk=None):
        """Mark service as completed"""
        service = self.get_object()
        if service.status not in ['pending', 'in_progress']:
            return Response(
                {'error': 'Service cannot be completed in this status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        service.status = 'completed'
        service.completion_time = timezone.now()
        service.save()
        return Response(ServiceRequestSerializer(service).data)


class ParkingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Parking Records"""
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all currently parked vehicles"""
        active_parking = Parking.objects.filter(status='active')
        serializer = self.get_serializer(active_parking, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """Check out a vehicle from parking"""
        parking = self.get_object()
        if parking.status != 'active':
            return Response(
                {'error': 'Vehicle is not currently parked'},
                status=status.HTTP_400_BAD_REQUEST
            )
        parking.status = 'completed'
        parking.check_out_time = timezone.now()

        # Calculate parking fee if not already set
        if not parking.parking_fee and 'parking_fee' in request.data:
            parking.parking_fee = request.data['parking_fee']

        parking.save()
        return Response(ParkingSerializer(parking).data)

    @action(detail=False, methods=['get'])
    def duration_stats(self, request):
        """Get parking duration statistics"""
        completed = Parking.objects.filter(status='completed', check_out_time__isnull=False)
        total_vehicles = completed.count()
        avg_duration = 0

        if total_vehicles > 0:
            duration_sum = sum([
                (p.check_out_time - p.check_in_time).total_seconds()
                for p in completed
            ])
            avg_duration = duration_sum / total_vehicles / 3600  # Convert to hours

        return Response({
            'total_vehicles_parked': total_vehicles,
            'average_duration_hours': round(avg_duration, 2),
        })


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """Filter payments"""
        queryset = Payment.objects.all()
        status = self.request.query_params.get('status')
        customer_id = self.request.query_params.get('customer_id')

        if status:
            queryset = queryset.filter(status=status)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        return queryset

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """Confirm a pending payment"""
        payment = self.get_object()
        if payment.status != 'pending':
            return Response(
                {'error': 'Only pending payments can be confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        payment.status = 'completed'
        if 'transaction_ref' in request.data:
            payment.transaction_ref = request.data['transaction_ref']
        payment.save()
        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=['get'])
    def daily_revenue(self, request):
        """Get daily revenue statistics"""
        today = timezone.now().date()
        today_payments = Payment.objects.filter(
            status='completed',
            payment_date__date=today
        )
        total_revenue = today_payments.aggregate(total=Sum('amount'))['total'] or 0
        transaction_count = today_payments.count()

        return Response({
            'date': today,
            'total_revenue': str(total_revenue),
            'transactions': transaction_count,
        })

    @action(detail=False, methods=['get'])
    def monthly_revenue(self, request):
        """Get monthly revenue statistics"""
        today = timezone.now()
        first_day = today.replace(day=1)
        monthly_payments = Payment.objects.filter(
            status='completed',
            payment_date__gte=first_day
        )
        total_revenue = monthly_payments.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'month': today.strftime('%B %Y'),
            'total_revenue': str(total_revenue),
            'transactions': monthly_payments.count(),
        })
