# Unity🌉Flask Auth Bridge

A production-ready Flask-based backend for an enterprise level application with enterprise-grade security features, authentication, rate limiting, and comprehensive user management.

## 🔍 Backend Architecture

The backend follows a modular, maintainable architecture:

- **Application Factory Pattern**: Enables flexible configuration across environments
- **PostgreSQL Database**: Robust relational database for enterprise data persistence
- **JWT Authentication**: Secure, stateless authentication system with role-based claims
- **Redis-backed Rate Limiting**: Prevents credential stuffing and DoS attacks
- **Comprehensive Error Handling**: Structured error responses with detailed internal logging

## 🛡️ Security Features

- **Bcrypt Password Hashing**: Industry-standard secure password storage
- **Account Lockout Mechanism**: Auto-locks accounts after consecutive failed login attempts
- **Rigorous Input Validation**: Prevents injection attacks with strict field validation
- **Distributed Rate Limiting**: Redis-backed request throttling with configurable limits
- **Short-lived JWT Tokens**: 1-hour access tokens with configurable expiry

## 🔄 API Endpoints

- **Authentication**
  - `/register` - User registration
  - `/login` - Authentication endpoint
  
- **User Operations**
  - `/profile` - Retrieve authenticated user profile
  
- **Admin Operations**
  - `/` (GET) - List all users (admin access)
  - `/` (POST) - Add new customer (admin access)
  - `/<account_number>` (PUT) - Update customer details
  - `/<account_number>` (DELETE) - Remove customer

- **System Monitoring**
  - `/health` - Application health check
  - `/db_check` - Database connectivity test

## 📋 Requirements

- Python 3.8+
- PostgreSQL 11+
- Redis 6+

## ⚙️ Basic Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hardikojha079/gatekeeper-auth.git
   cd gatekeeper-auth
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_NAME=your_db_name
   JWT_SECRET_KEY=your_secret_key
   REDIS_URL=redis://localhost:6379/0
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Start the development server:
   ```bash
   python run.py
   ```

## 🚀 Enterprise Deployment Guide

### 1. Containerization

Create Docker infrastructure:

```bash
# Create Dockerfile
docker build -t enterprise-api:latest .

# Run with Docker Compose
docker-compose up -d
```

### 2. Database Scaling

Implement connection pooling:

```python
# Update config.py with connection pool settings
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

### 3. Production WSGI Server

Replace development server:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### 4. Load Balancing

Deploy behind Nginx for load balancing:

```
# nginx.conf example
upstream gatekeeper_auth {
    server app1:5000;
    server app2:5000;
    server app3:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://gatekeeper_auth;
    }
}
```

### 5. Security Hardening

Implement additional security:

- Set up HTTPS with Let's Encrypt
- Configure CSP headers
- Add API key authentication for partners
- Implement OAuth 2.0 for third-party integrations

### 6. Monitoring & Alerting

Add observability infrastructure:

```bash
# Install Prometheus client
pip install prometheus-client

# Configure Prometheus metrics in app
```

Connect with monitoring stack (Prometheus, Grafana, ELK).

### 7. CI/CD Pipeline

Create automated deployment pipeline with GitHub Actions or Jenkins:
- Automated testing
- Security scanning
- Containerization
- Blue/green deployment

## 📦 Dependencies

- Flask - Web framework
- Flask-SQLAlchemy - ORM
- Flask-JWT-Extended - Authentication
- Flask-Migrate - Database migrations
- Flask-Limiter - Rate limiting
- PostgreSQL - Relational database
- Redis - Caching and rate limiting
- Bcrypt - Password hashing

---

# Unity Enterprise Application Frontend

## Overview

This Unity frontend provides a modular interface for interacting with our robust API backend. The system implements user authentication with JWT tokens and lays the groundwork for a complete application. Currently, only the login authentication UI has been fully implemented, while the registration and admin interfaces are ready for development.

## Architecture

The frontend consists of several modular components:

1. **APIManager**: Handles all API communication and token management
2. **RequestHelper**: Utility for HTTP requests (GET, POST, PUT, DELETE)
3. **Model Classes**: Serializable data structures for API communication
4. **Endpoints**: Configuration for API URLs
5. **AuthUI**: User interface for authentication
6. **Logger**: Utility for consistent logging

## Implemented Features

- **Login Authentication**: Complete UI and functionality for user login
- **JWT Token Management**: Secure storage and handling of authentication tokens
- **API Communication Framework**: Infrastructure for all backend endpoints
- **Profile Data Access**: Functions to retrieve user profile information
- **User Management API**: Methods for updating and deleting users

## For Developers

### Important Note
This implementation only includes the login UI. To fully utilize the backend capabilities, you'll need to implement:

1. **Registration UI**: Interface for new user registration (backend endpoint ready)
2. **Admin Dashboard**: Interface for user management functions that are already accessible via the API
3. **User Profile UI**: Interface to display and edit profile data (API methods already implemented)

## System Robustness

The combined frontend-backend architecture offers exceptional stability and security:

- **Layered Authentication**: Frontend token management paired with backend JWT verification
- **Clean Separation**: UI components isolated from business logic and API communication
- **Flexible Architecture**: Easy to extend with new features without compromising existing functionality
- **Comprehensive Backend**: Ready-made endpoints for user operations with corresponding frontend API methods
- **Error Resilience**: Structured error handling between frontend and backend

## Future Enhancements

1. **Complete UI Implementation**: Finish registration and admin interfaces
2. **Token Refresh Mechanism**: Add automatic handling of token expiration
3. **Form Validation**: Add client-side validation before API requests
4. **Loading States**: Implement visual indicators during API calls
5. **Notification System**: Display backend alerts and messages
6. **Remember Me Functionality**: Add option to persist login sessions

## Usage Example

```csharp
// Login and retrieve profile data
apiManager.Login(new LoginRequest(accountNumber, password), response => {
    if (response.Contains("successful")) {
        apiManager.FetchProfile(profileData => {
            // Process profile information
        });
    }
});
```
