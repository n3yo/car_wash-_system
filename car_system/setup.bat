@echo off
REM Smart Car Wash System Setup Script for Windows

echo.
echo ======================================
echo Smart Car Wash & Parking System
echo Setup Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] Python found

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Copy environment file
echo.
echo Setting up environment configuration...
if not exist .env (
    copy .env.example .env
    echo [OK] .env file created (please update database credentials)
) else (
    echo [INFO] .env file already exists
)

REM Run migrations
echo.
echo Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run migrations
    pause
    exit /b 1
)

echo [OK] Database migrations completed

REM Create superuser
echo.
echo Creating superuser account...
python manage.py createsuperuser

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Make sure PostgreSQL is installed and running
echo 2. Update .env with your database credentials
echo 3. Run: python manage.py runserver
echo 4. Visit: http://localhost:8000/admin/
echo.
pause
