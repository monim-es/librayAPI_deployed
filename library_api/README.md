# 📚 Library Management API

A simple Django REST API that manages users, books, and borrowing transactions using **JWT authentication**.

---

## 🚀 Features

- 👥 **User Management** — Register, login, and view profiles  
- 🛡️ **Admin Control** — Manage users and books (CRUD)  
- 📘 **Book Management** — Users can view; admins can add/update/delete  
- 🔁 **Transactions** — Users can borrow and return books  
- 🔐 **JWT Authentication** — Tokens expire in 1 hour  
- 🧭 **Swagger UI** — Explore and test endpoints easily  

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/monim-es/library_api
cd library_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## 🌐 API Endpoints

| Endpoint | Method | Description | Auth | Role |
|----------|--------|-------------|------|------|
| `/api/register/` | POST | Register a new user | ❌ | Any |
| `/api/token/` | POST | Login to get JWT tokens | ❌ | Any |
| `/api/token/refresh/` | POST | Refresh JWT token | ❌ | Any |
| `/api/users/` | GET | List all users | ✅ | Admin |
| `/api/books/` | GET | View all books | ✅ | User/Admin |
| `/api/books/<id>/` | GET | View book details | ✅ | User/Admin |
| `/api/books/` | POST | Add a book | ✅ | Admin |
| `/api/transactions/` | POST | Borrow (checkout) a book | ✅ | User |
| `/api/transactions/<id>/return/` | PUT | Return a borrowed book | ✅ | User |
| `/swagger/` | GET | API documentation (Swagger UI) | ❌ | Any |

---

## 🧾 Example Requests

### Register

```json
POST /api/register/
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "mypassword",
  "profile": {
    "phone_number": "0612345678",
    "address": "123 Main St",
    "date_of_birth": "2000-05-10"
  }
}
```

### Login

```json
POST /api/token/
{
  "username": "john_doe",
  "password": "mypassword"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use JWT in Headers

```
Authorization: Bearer <access_token>
```

### Borrow a Book

```json
POST /api/transactions/
{
  "book": 1
}
```

### Return a Book

```json
PUT /api/transactions/1/return/
```

---

## ⚙️ Logic Summary

- Users register and log in using JWT tokens.
- Admins can manage all users and books.
- Users can only view books and borrow/return them.
- Borrowing decreases `available_copies`; returning increases it.
- Users can't borrow the same book twice before returning it.

---

## 🧩 Tech Stack

- **Django** — Backend framework
- **Django REST Framework** — API building
- **SimpleJWT** — Token authentication
- **drf-yasg** — Swagger documentation
- **SQLite** — Database

---

## 📖 Swagger Access

🔗 **http://localhost:8000/swagger/**

- Authorize with your JWT access token.
- Test all endpoints interactively.

---

## 👩‍💻 Author

**Monim Es-Sraoui**

---
