# Kickoff — Futsal Management System

A beginner-friendly Django platform for futsal venues, players, teams, and bookings.

## What is included

- Secure user registration, login, and logout
- Venue and court management through Django admin
- Public court discovery and real-time available-slot display
- Booking flow with collision prevention
- Booking calendar, booking confirmations, and receipt view
- Team and player management
- Tournament listing and registration
- Payment record and a simple owner dashboard/report

## Get started

1. Install Python 3.11+ and PostgreSQL.
2. Create a virtual environment: `py -m venv .venv`
3. Activate it in PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install packages: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`, then set your database details. If `DATABASE_URL` is not present, the project uses a local SQLite database for learning.
6. Run `py manage.py makemigrations` and `py manage.py migrate`
7. Create an admin user: `py manage.py createsuperuser`
8. Start the site: `py manage.py runserver`

Visit `/admin/` to add venues, courts, pricing, and tournaments. Visit `/dashboard/` after logging in to manage bookings and teams.

## PostgreSQL database

Create the database first:

```sql
CREATE DATABASE futsal_management;
```

Use this in `.env`:

```text
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/futsal_management
```

