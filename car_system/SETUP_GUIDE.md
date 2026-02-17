# 🚀 Smart Car Wash System - Complete Setup & Usage Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Configuration](#database-configuration)
4. [Running the Application](#running-the-application)
5. [API Usage Examples](#api-usage-examples)
6. [Common Tasks](#common-tasks)

---

## 📦 Prerequisites

### Windows
- Python 3.8+ (download from [python.org](https://www.python.org/downloads/))
- PostgreSQL 10+ (download from [postgresql.org](https://www.postgresql.org/download/windows/))

### macOS
- Homebrew (optional)
- Python 3.8+ (`brew install python`)
- PostgreSQL 10+ (`brew install postgresql`)

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install python3 python3-pip postgresql postgresql-contrib
```

---

## 💾 Installation

### Using Windows Setup Script (Easiest for Windows)
```bash
setup.bat
```

### Manual Installation

#### Windows
```bash
cd car_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
```

#### macOS/Linux
```bash
cd car_system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
```

---

## 🗄️ Database Configuration

### Create PostgreSQL Database and User

```sql
CREATE DATABASE carwash_db;
CREATE USER carwash_user WITH PASSWORD 'your_secure_password';
ALTER ROLE carwash_user SET client_encoding TO 'utf8';
ALTER ROLE carwash_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE carwash_db TO carwash_user;
```

### Update .env File
```
DB_NAME=carwash_db
DB_USER=carwash_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secure-random-string
DEBUG=True
```

---

## ▶️ Running the Application

```bash
# Activate virtual environment
venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)

# Start development server
python manage.py runserver

# Access in browser
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/api/
```

---

## 🔌 API Usage Examples

### Create Customer
```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "phone": "+255712345678",
    "email": "jane@example.com",
    "id_number": "ID123456",
    "address": "Dar es Salaam"
  }'
```

### Register Vehicle
```bash
curl -X POST http://localhost:8000/api/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1,
    "plate_number": "TZA-1234-ABC",
    "vehicle_type": "sedan",
    "make": "Toyota",
    "model": "Camry",
    "year": 2020,
    "color": "black"
  }'
```

### Get Daily Revenue
```bash
curl http://localhost:8000/api/payments/daily-revenue/
```

---

## 🛠️ Common Commands

```bash
python manage.py test carwash              # Run tests
python manage.py makemigrations             # Create migrations
python manage.py migrate                    # Apply migrations
python manage.py createsuperuser            # Create admin
python manage.py shell                      # Python shell
```

---

**System is ready to use!** 🚀
