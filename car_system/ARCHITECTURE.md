# 🏗️ Smart Car Wash System - Architecture & Workflows

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                       │
│         (Web/Mobile/Desktop - Uses REST API)                │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST Requests
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Django REST Framework API Layer                 │
├─────────────────────────────────────────────────────────────┤
│  Endpoints: /api/customers, /api/vehicles, /api/payments   │
│  Features: Serialization, Pagination, Filtering             │
└────────────┬──────────────────────────────────────────────┬──┘
             │                                               │
   ViewSets  │          Serializers                         │
             │                                               │
┌────────────▼──────────────────────────────────────────────▼──┐
│                  Django Application Layer                     │
├───────────────────────────────────────────────────────────────┤
│  Views: AttendantViewSet, CustomerViewSet, VehicleViewSet... │
│  Models: 7 core models with relationships                     │
│  Admin: Customized Django Admin Interface                     │
└────────────┬─────────────────────────────────────────────────┘
             │ ORM Queries
             ▼
┌───────────────────────────────────────────────────────────────┐
│                PostgreSQL Database                             │
├───────────────────────────────────────────────────────────────┤
│  Tables: customers, vehicles, services, parking, payments... │
└───────────────────────────────────────────────────────────────┘
```

---

## 🔄 Service Workflow

```
CUSTOMER ARRIVAL
    │
    ├─→ Vehicle Check-in (Parking)
    │   └─→ Create Parking Record
    │       ├─ Vehicle ID
    │       ├─ Customer ID
    │       ├─ Check-in Time (NOW)
    │       └─ Status: "active"
    │
    └─→ Request Service
        │
        ├─→ Create ServiceRequest
        │   ├─ Vehicle ID
        │   ├─ Customer ID
        │   ├─ Service Type ID
        │   ├─ Assign Attendant
        │   └─ Status: "pending"
        │
        ├─→ Service In Progress
        │   ├─ Update Status → "in_progress"
        │   ├─ Set Start Time
        │   └─ Perform Service
        │
        └─→ Service Complete
            ├─ Update Status → "completed"
            ├─ Set Completion Time
            └─ Ready for Payment

PAYMENT & CHECKOUT
    │
    ├─→ Create Payment Record
    │   ├─ Link Service Request
    │   ├─ Amount: Service Price
    │   ├─ Payment Method
    │   └─ Status: "pending"
    │
    ├─→ Confirm Payment
    │   ├─ Update Status → "completed"
    │   ├─ Add Transaction Reference
    │   └─ Update Revenue
    │
    └─→ Vehicle Check-out
        ├─ Update Parking Status → "completed"
        ├─ Set Check-out Time
        └─ Vehicle Released
```

---

## 📊 Core Workflows

### Workflow 1: Car Wash Service

```
[START] → [Customer Registration] → [Vehicle Registration]
    │
    └─→ [Create Service Request]
        ├─ Select Service Type
        ├─ Assign Attendant
        └─ Status: pending
            │
            ├─→ [Start Service]
            │   └─ Status: in_progress
            │
            ├─→ [Complete Service]
            │   └─ Status: completed
            │
            └─→ [Create Payment]
                ├─ Link Service Request
                ├─ Set Amount
                ├─ Select Payment Method
                │
                └─→ [Confirm Payment]
                    └─ Payment Complete
                        │
                        └─→ [END] Service Delivered
```

### Workflow 2: Parking Management

```
[START] → [Vehicle Check-In]
    │
    └─→ [Create Parking Record]
        ├─ Vehicle ID
        ├─ Customer ID
        ├─ Check-in Time: NOW
        └─ Status: active
            │
            └─→ [Vehicle Parked]
                │
                ├─→ [Duration]
                │   └─ Time passes...
                │
                └─→ [Vehicle Check-Out]
                    ├─ Set Check-out Time
                    ├─ Calculate Duration
                    │
                    └─→ [Calculate Parking Fee]
                        ├─ Set Parking Fee
                        └─ Status: completed
                            │
                            └─→ [Create Payment]
                                │
                                └─→ [Confirm Payment]
                                    │
                                    └─→ [END] Vehicle Released
```

---

## 🎯 Status Transitions

### ServiceRequest Status Flow

```
STATES:
┌─────────┐
│ pending │ ← Initial state when created
└────┬────┘
     │ start_service() called
     ▼
┌──────────────┐
│ in_progress  │ ← Service is being delivered
└────┬─────────┘
     │ complete_service() called
     │
     ├─────────────────────────────┐
     ▼                             ▼
┌──────────────┐           ┌───────────────┐
│  completed   │           │   cancelled   │
└──────────────┘           └───────────────┘
   ↓ Ready for                ↓ Service
   Payment                    Aborted
```

### Parking Status Flow

```
┌─────────┐
│ active  │ ← Vehicle currently parked
└────┬────┘
     │ check_out() called
     ▼
┌──────────────┐
│  completed   │ ← Vehicle retrieved
└──────────────┘
```

### Payment Status Flow

```
┌─────────┐
│ pending │ ← Payment created
└────┬────┘
     │
     ├──[confirm_payment]──┐
     │                     ▼
     │                ┌───────────┐
     │                │ completed │ ← Success
     │                └───────────┘
     │
     ├──[cancel]──────┐
     │                ▼
     │            ┌──────────┐
     │            │ failed   │ ← Transaction Failed
     │            └──────────┘
     │
     └──[refund]──┐
                  ▼
             ┌──────────┐
             │ refunded │ ← Refunded
             └──────────┘
```

---

## 🔗 Entity Relationships

```
ATTENDANT                          CUSTOMER (Hub)
├─ Manages ──→ ServiceRequest      ├─ Owns ────→ Vehicle
└─ Handles ──→ Parking             ├─ Requests → ServiceRequest
                                    ├─ Parks ───→ Parking
                                    └─ Makes ───→ Payment

                    VEHICLE
                    ├─ receives ────→ ServiceRequest
                    └─ has ─────────→ Parking


SERVICE TYPE ──→ ServiceRequest ──→ Payment (1:1)
              
PARKING ──────────→ Payment (1:1)
```

---

## 📈 Key Features per ViewSet

### AttendantViewSet
- List all attendants
- Get attendant details
- **Custom**: Performance metrics (services completed, parking handled)

### CustomerViewSet
- CRUD customers
- **Custom**: Customer summary with total spent and recent history

### VehicleViewSet
- CRUD vehicles
- **Custom**: Service history for specific vehicle
- **Filter**: By customer_id

### ServiceTypeViewSet
- List active services
- Create new service types

### ServiceRequestViewSet
- CRUD service requests
- **Custom Endpoints**:
  - `/pending/` - Get all pending requests
  - `/{id}/start-service/` - Change status to in_progress
  - `/{id}/complete-service/` - Mark as completed

### ParkingViewSet
- CRUD parking records
- **Custom Endpoints**:
  - `/active/` - Currently parked vehicles
  - `/{id}/check-out/` - Vehicle checkout
  - `/duration-stats/` - Parking statistics

### PaymentViewSet
- CRUD payments
- **Custom Endpoints**:
  - `/{id}/confirm-payment/` - Mark as completed
  - `/daily-revenue/` - Today's revenue
  - `/monthly-revenue/` - Month's revenue
- **Filters**: status, customer_id

---

## 💰 Revenue Calculation

```
DAILY REVENUE = SUM(Payment.amount) 
WHERE status='completed' AND payment_date=TODAY

MONTHLY REVENUE = SUM(Payment.amount) 
WHERE status='completed' AND payment_date >= FIRST_DAY_OF_MONTH

BY SERVICE TYPE = SUM(Payment.amount) GROUP BY ServiceType
BY PAYMENT METHOD = SUM(Payment.amount) GROUP BY PaymentMethod
BY CUSTOMER = SUM(Payment.amount) GROUP BY Customer
```

---

## 🔐 Data Security

- Django ORM prevents SQL injection
- CSRF middleware for form protection
- CORS headers configured
- Environment variables for secrets
- Audit trail (created_at, updated_at on all models)

---

**Architecture Document Complete** ✅
