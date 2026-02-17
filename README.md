# EasyEcom Django Backend

## Features
- Shipment CRUD API
- Shipment Status management
- Custom actions:
  - Send to carrier (marks In Transit)
  - Mark as Delivered
  - Mark as Failed

## Tech Stack
- Django
- Django REST Framework
- SQLite (for development)

## How to Run

1. Clone the repo
2. Create virtual environment
3. Install requirements:
   pip install -r requirements.txt
4. Run migrations:
   python manage.py migrate
5. Start server:
   python manage.py runserver

API runs on:
http://127.0.0.1:8000/

