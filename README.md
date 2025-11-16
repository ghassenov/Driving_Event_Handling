# Driving_Event_Handling - FastAPI Backend

A FastAPI backend for a driver monitoring system that handles user authentication, sensor data processing, and driving event detection.

---

## Features

- **JWT Authentication** - Secure user registration and login
- **Sensor Data Processing** - Handle accelerometer, gyroscope, and magnetometer data coming from phone sensors.
- **Driving Event Detection** - Analyze sensor data to detect driving events
- **RESTful API** - API endpoints for mobile app integration
- **SQLite Database** - Lightweight database for user and trip data (For the time being)

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **JWT** - JSON Web Token authentication
- **Argon2** - Secure password hashing
- **Uvicorn** - ASGI web server
- **Pydantic** - Data validation

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ghassenov/Driving_Event_Handling.git
cd Driving_Event_Handling
```
### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Environment Configuration
Create a .env file in the root directory
```bash
DATABASE_URL=sqlite:///./app.db
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
```
### 5. Run the application
```bash
uvicorn app.main:app --reload
```

## API Documentation
Once running, access the interactive API docs:
- Swagger UI: /docs
- ReDoc: /redoc
