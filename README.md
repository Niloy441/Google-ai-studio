# OTP Auth System

A Django-based authentication system using phone numbers and OTP.

## Features
- Signup/Login with Phone Number
- Custom User Model
- Secure OTP Hashing
- Internal Admin Console for OTP viewing (Dev mode)
- Swappable OTP Providers
- Rate Limiting & Security best practices

## Tech Stack
- Django 5.0
- PostgreSQL
- Redis & Celery
- Vanilla JS & CSS

## Setup Instructions

1. **Clone and install dependencies:**
   ```bash
   pip install -r requirements/dev.txt
   ```

2. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in the values.

3. **Database Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser (for Console access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

6. **Run Celery (for background tasks):**
   ```bash
   celery -A config worker -l info
   ```

## OTP Verification in Dev Mode
When you request an OTP during signup or login, go to `/console/dashboard/` (login as admin) to see the generated code.
