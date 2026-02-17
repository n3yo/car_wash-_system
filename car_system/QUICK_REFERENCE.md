# 🎯 Smart Car Wash System - Quick Reference

## 🚀 Quick Start (5 Minutes)

### Windows
```bash
setup.bat
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📊 Key API Endpoints

### Base: `/api/`

| Resource | List | Create | Detail | Custom |
|----------|------|--------|--------|--------|
| Customers | GET `/customers/` | POST | GET `/customers/{id}/` | `/summary/` |
| Vehicles | GET `/vehicles/` | POST | GET `/vehicles/{id}/` | `/service-history/` |
| Services | GET `/services/` | POST | - | - |
| Service Requests | GET `/service-requests/` | POST | GET `/{id}/` | `/pending/`, `/start-service/`, `/complete-service/` |
| Parking | GET `/parking/` | POST | GET `/parking/{id}/` | `/active/`, `/check-out/`, `/duration-stats/` |
| Payments | GET `/payments/` | POST | GET `/payments/{id}/` | `/confirm-payment/`, `/daily-revenue/`, `/monthly-revenue/` |
| Attendants | GET `/attendants/` | POST | GET `/{id}/` | `/performance/` |

---

## 📝 Database Models

```
Customer ──────┬──→ Vehicle
               ├──→ ServiceRequest
               ├──→ Parking
               └──→ Payment

Vehicle ───────┬──→ ServiceRequest
               └──→ Parking

ServiceType ───→ ServiceRequest
Attendant ──┬──→ ServiceRequest
            └──→ Parking

ServiceRequest → Payment (1:1)
Parking ────────→ Payment (1:1)
```

---

## ✨ Sample Workflow

### 1. Register Customer
```bash
POST /api/customers/
{
  "name": "David",
  "phone": "+255712345678",
  "email": "david@example.com",
  "id_number": "ID001",
  "address": "Dar es Salaam"
}
```

### 2. Register Vehicle
```bash
POST /api/vehicles/
{
  "customer": 1,
  "plate_number": "TZA-1234-ABC",
  "make": "Toyota",
  "model": "Camry",
  "year": 2020,
  "vehicle_type": "sedan",
  "color": "black"
}
```

### 3. Create Service Request
```bash
POST /api/service-requests/
{
  "vehicle": 1,
  "customer": 1,
  "service_type": 1,
  "attendant": 1
}
```

### 4. Start Service
```bash
POST /api/service-requests/1/start-service/
```

### 5. Complete Service
```bash
POST /api/service-requests/1/complete-service/
```

### 6. Create Payment
```bash
POST /api/payments/
{
  "customer": 1,
  "service_request": 1,
  "amount": 50000.00,
  "payment_method": "cash"
}
```

### 7. Confirm Payment
```bash
POST /api/payments/1/confirm-payment/
{
  "transaction_ref": "TXN001"
}
```

---

## 🗂️ File Structure

```
car_system/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── setup.bat             # Windows setup
├── .env.example          # Environment template
├── README.md             # Full documentation
├── config/               # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── carwash/             # Main app
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── admin.py
    ├── urls.py
    ├── tests.py
    └── migrations/
```

---

## 🛠️ Commands

```bash
# Server
python manage.py runserver              # Start dev server
python manage.py runserver 8080         # On different port

# Testing
python manage.py test carwash           # Run tests
python manage.py test carwash.tests.CustomerModelTest  # Specific test

# Database
python manage.py migrate                # Apply migrations
python manage.py makemigrations         # Create migrations

# Admin
python manage.py createsuperuser        # Create admin user
python manage.py changepassword user    # Change password

# Data
python manage.py shell                  # Python shell
python manage.py dumpdata carwash > backup.json  # Backup
python manage.py loaddata backup.json   # Restore
```

---

## 🔐 Configuration

Edit `.env`:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=carwash_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

## ✅ Access Points

- **Admin Dashboard**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/
- **Django Admin**: Create superuser to access

---

**Ready to build!** 🚀
