# 📁 Smart Car Wash System - Project Structure

## Directory Tree

```
car_system/
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── setup.bat             # Windows setup automation
├── .env.example          # Environment variables template
│
├── README.md             # Main documentation
├── SETUP_GUIDE.md        # Setup instructions
├── QUICK_REFERENCE.md    # Quick API reference
└── PROJECT_STRUCTURE.md  # This file
│
├── config/               # Django project configuration
│   ├── __init__.py
│   ├── settings.py       # Database, apps, middleware settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI application entry point
│
├── carwash/             # Main Django application
│   ├── migrations/       # Database migration files
│   │   └── __init__.py
│   │
│   ├── __init__.py
│   ├── admin.py         # Django admin customization
│   ├── apps.py          # App configuration
│   ├── models.py        # Database models (7 models)
│   ├── views.py         # DRF ViewSets (40+ endpoints)
│   ├── serializers.py   # DRF Serializers
│   ├── urls.py          # App URL routing
│   ├── tests.py         # Unit tests
│   └── forms.py         # Django forms (optional, for HTML UI)
│
└── templates/           # HTML templates (optional, for web interface)
    └── (future web UI files)
```

---

## 📦 Key Components

### 1. **Django Models** (`carwash/models.py`)

| Model | Purpose | Relationships |
|-------|---------|---------------|
| **Attendant** | Staff/Employees | (1:M) ServiceRequest, (1:M) Parking |
| **Customer** | Vehicle Owners | (1:M) Vehicle, (1:M) ServiceRequest, (1:M) Parking, (1:M) Payment |
| **Vehicle** | Car Information | (M:1) Customer, (1:M) ServiceRequest, (1:M) Parking |
| **ServiceType** | Available Services | (1:M) ServiceRequest |
| **ServiceRequest** | Service Orders | (M:1) Vehicle, (M:1) Customer, (M:1) ServiceType, (M:1) Attendant, (1:1) Payment |
| **Parking** | Parking Records | (M:1) Vehicle, (M:1) Customer, (M:1) Attendant, (1:1) Payment |
| **Payment** | Payment Transactions | (M:1) Customer, (1:1) ServiceRequest (opt), (1:1) Parking (opt) |

### 2. **API Endpoints** (`carwash/views.py`)

ViewSets with 40+ endpoints:
- **AttendantViewSet**: CRUD + performance metrics
- **CustomerViewSet**: CRUD + customer summary
- **VehicleViewSet**: CRUD + service history
- **ServiceTypeViewSet**: List/Create services
- **ServiceRequestViewSet**: CRUD + status management + custom actions
- **ParkingViewSet**: CRUD + check-in/check-out + statistics
- **PaymentViewSet**: CRUD + confirm payment + revenue reports

### 3. **Serializers** (`carwash/serializers.py`)

JSON serializers for all models:
- Customer serialization with related data
- Vehicle with customer name
- Service requests with all related details
- Parking records with attendant info
- Payment serialization with linked objects

### 4. **Admin Interface** (`carwash/admin.py`)

Customized admin for all models:
- List displays with key fields
- Filters and search capabilities
- Fieldset grouping
- Read-only audit trails (created_at, updated_at)

### 5. **Configuration** (`config/settings.py`)

- PostgreSQL database connection
- REST Framework settings
- CORS headers for API access
- Static and media file handling
- Authentication framework

---

## 🔄 Data Flow Architecture

```
HTTP Request
    ↓
Django URL Router (config/urls.py, carwash/urls.py)
    ↓
ViewSet (carwash/views.py)
    ↓
Django ORM
    ↓
PostgreSQL Database
    ↓
(Response Path)
Serializer (carwash/serializers.py)
    ↓
JSON Response
```

---

## 🔌 Technology Stack Details

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Django 4.2.8 | Web framework |
| **API** | DRF 3.14.0 | REST API |
| **Database** | PostgreSQL | Data persistence |
| **Driver** | psycopg2 | PostgreSQL connector |
| **Config** | python-decouple | Environment management |
| **CORS** | django-cors-headers | Cross-origin requests |
| **Images** | Pillow | Image handling |

---

## 🔐 Security Features

- CSRF protection middleware
- SQL injection prevention (Django ORM)
- XSS protection
- CORS configuration
- Authentication-ready framework
- Environment variable protection (.env)

---

## 📊 Database Schema Highlights

All models include:
- `id` (Primary Key - Auto)
- `created_at` (DateTime - Auto)
- `updated_at` (DateTime - Auto)

Special date fields:
- ServiceRequest: `request_date`, `start_time`, `completion_time`
- Parking: `check_in_time`, `check_out_time`
- Customer: `date_registered`
- Attendant: `hire_date`

---

## 🚀 Scalability Path

| Stage | Action | Tools |
|-------|--------|-------|
| Development | Single server | Django dev server |
| Testing | Test suite | pytest, coverage |
| Staging | Full deployment | Gunicorn, Nginx |
| Production | Enterprise setup | Load balancer, Redis cache, CDN |

---

## 📝 File Purposes

| File | Purpose |
|------|---------|
| `manage.py` | Django management commands entry point |
| `requirements.txt` | Python package dependencies |
| `setup.bat` | Windows automated setup script |
| `.env.example` | Environment variables template |
| `config/settings.py` | Django configuration |
| `config/urls.py` | Main URL routing |
| `config/wsgi.py` | WSGI application |
| `carwash/models.py` | Database model definitions |
| `carwash/views.py` | API endpoints and logic |
| `carwash/serializers.py` | JSON serialization |
| `carwash/admin.py` | Admin interface |
| `carwash/urls.py` | App-level routing |
| `carwash/tests.py` | Unit tests |

---

## 🔄 Request/Response Flow Example

### Create Service Request

```
Request:
POST /api/service-requests/
{
  "vehicle": 1,
  "customer": 1,
  "service_type": 1,
  "attendant": 1
}
    ↓
Processing:
1. Django routes to ServiceRequestViewSet.create()
2. ServiceRequestSerializer validates data
3. Django ORM creates ServiceRequest record
4. Returns created object
    ↓
Response:
{
  "id": 1,
  "vehicle": 1,
  "vehicle_plate": "TZA-1234-ABC",
  "customer": 1,
  "customer_name": "David",
  "attendant": 1,
  "attendant_name": "John",
  "service_type": 1,
  "service_name": "Basic Wash",
  "status": "pending",
  "request_date": "2026-02-16T10:30:00Z",
  "...": "..."
}
```

---

**Architecture Complete** ✅
