# 🚗 Smart Car Wash & Parking System

A comprehensive Django-based system for managing car wash services and parking facilities. Built with Django REST Framework and PostgreSQL.

## 📋 Features

- **🚗 Vehicle Management**: Track vehicles by plate number, make, model, and owner
- **👤 Customer Management**: Store customer information (owner, phone, email, ID)
- **🧼 Service Tracking**: Manage different car wash services (basic wash, interior clean, engine wash, etc.)
- **🅿️ Parking Management**: Track vehicle parking with check-in/check-out times
- **💰 Payment Processing**: Handle payments for services and parking
- **📅 Date & Time Tracking**: Complete audit trail with timestamps
- **👨‍💼 Attendant Management**: Assign attendants to services and parking
- **📊 Reports & Analytics**: Daily/monthly revenue, parking statistics, attendant performance

## 🛠️ Technology Stack

- **Backend**: Django 4.2.8
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Authentication**: Django Auth (extensible)
- **CORS Support**: django-cors-headers

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 10+
- pip (Python package manager)

### Steps

1. **Navigate to project directory**
```bash
cd car_system
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
# Update database credentials, secret key, etc.
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser (admin account)**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📚 API Endpoints

### Base URL: `/api/`

#### Attendants
- `GET /attendants/` - List all attendants
- `POST /attendants/` - Create new attendant
- `GET /attendants/{id}/` - Get attendant details
- `GET /attendants/{id}/performance/` - Get attendant performance stats

#### Customers
- `GET /customers/` - List all customers
- `POST /customers/` - Create new customer
- `GET /customers/{id}/` - Get customer details
- `GET /customers/{id}/summary/` - Get customer summary with history

#### Vehicles
- `GET /vehicles/` - List all vehicles
- `POST /vehicles/` - Register new vehicle
- `GET /vehicles/{id}/` - Get vehicle details
- `GET /vehicles/{id}/service-history/` - View service history
- Filter: `?customer_id=1`

#### Services
- `GET /services/` - List available services
- `POST /services/` - Create new service type

#### Service Requests
- `GET /service-requests/` - List all service requests
- `POST /service-requests/` - Create new service request
- `GET /service-requests/pending/` - Get pending requests
- `POST /service-requests/{id}/start-service/` - Start service
- `POST /service-requests/{id}/complete-service/` - Complete service

#### Parking
- `GET /parking/` - List all parking records
- `POST /parking/` - Check in vehicle
- `GET /parking/active/` - View currently parked vehicles
- `POST /parking/{id}/check-out/` - Check out vehicle
- `GET /parking/duration-stats/` - View parking statistics

#### Payments
- `GET /payments/` - List all payments
- `POST /payments/` - Create payment record
- `POST /payments/{id}/confirm-payment/` - Confirm payment
- `GET /payments/daily-revenue/` - Get today's revenue
- `GET /payments/monthly-revenue/` - Get monthly revenue
- Filter: `?status=completed&customer_id=1`

## 📊 Admin Interface

Access Django admin at `/admin/`
- Full CRUD operations for all models
- Advanced filtering and search
- Bulk actions

## 🗄️ Database Models

### Core Models

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Attendant** | Staff/Employees | name, phone, email, id_number, hire_date |
| **Customer** | Vehicle Owners | name, phone, email, id_number, address |
| **Vehicle** | Car Information | plate_number, make, model, year, customer |
| **ServiceType** | Available Services | name, base_price, estimated_time |
| **ServiceRequest** | Service Orders | vehicle, customer, service_type, status |
| **Parking** | Parking Records | vehicle, customer, check_in, check_out, fee |
| **Payment** | Payment Records | customer, amount, method, status |

## 🚀 Quick Start Commands

```bash
# Run tests
python manage.py test carwash

# Create migrations after model changes
python manage.py makemigrations

# Load sample data
python manage.py shell < carwash/sample_data.py

# Access Django shell
python manage.py shell

# View installed apps
python manage.py showmigrations
```

---

**Built with ❤️ for Car Wash Businesses**
