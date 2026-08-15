# Authentication Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Medium

---

# 1. Purpose

Authentication protects all APIs of the Medical Store Management System.

Only authenticated users can access the backend.

This module is intentionally kept simple because the current version is a Proof of Concept (POC).

No advanced authentication features are included.

---

# 2. Scope

Included

✔ Login

✔ Logout

✔ JWT Authentication

✔ Token Refresh

✔ Current User

Excluded

✘ User Registration

✘ User Management

✘ Forgot Password

✘ Email Verification

✘ OTP

✘ Social Login

✘ Two Factor Authentication

These features may be added in future versions.

---

# 3. Authentication Flow

User

↓

Enter Username

↓

Enter Password

↓

Backend Validation

↓

Generate JWT Token

↓

Return Token

↓

Frontend Stores Token

↓

Authenticated Requests

---

# 4. Authentication Method

Authentication Type

JWT

Authorization Header

Bearer <access_token>

Every protected API requires a valid JWT Access Token.

---

# 5. Login Process

Step 1

User submits

Username

Password

↓

Step 2

Validate credentials

↓

Step 3

Generate

Access Token

Refresh Token

↓

Step 4

Return response

Example Response

{
    "success": true,
    "message": "Login successful.",
    "data": {
        "access": "...",
        "refresh": "..."
    }
}

---

# 6. Logout

JWT is stateless.

Logout is handled on frontend by removing stored tokens.

Optional future enhancement

Blacklist Refresh Tokens.

---

# 7. Token Refresh

When Access Token expires

↓

Frontend sends Refresh Token

↓

Backend validates

↓

Returns new Access Token

No login required again.

---

# 8. Protected APIs

The following modules require authentication.

Medicine

Supplier

Purchase

Inventory

Sales

Dashboard

Reports

Every request without a valid token returns

401 Unauthorized

---

# 9. User Model

POC uses Django's default User model.

No custom user model is required.

Required Fields

Username

Password

is_active

is_staff

No additional profile information is stored.

---

# 10. Initial Admin User

The system contains one administrator account.

Responsibilities

Manage Medicines

Manage Purchases

Manage Inventory

View Reports

Manage Dashboard

Additional users can be created manually through Django Admin if required.

No in-app user creation is available.

---

# 11. Validation Rules

Username cannot be empty.

Password cannot be empty.

Inactive users cannot log in.

Invalid credentials return

401 Unauthorized.

---

# 12. Security Rules

Passwords are never stored in plain text.

Passwords are always hashed by Django.

Access Token should never be stored in database.

Refresh Token should never be exposed in logs.

---

# 13. API Endpoints

POST

/api/v1/auth/login/

POST

/api/v1/auth/refresh/

POST

/api/v1/auth/logout/

GET

/api/v1/auth/me/

---

# 14. Response Format

Success

{
    "success": true,
    "message": "Login successful.",
    "data": {}
}

Failure

{
    "success": false,
    "message": "Invalid username or password.",
    "errors": {}
}

---

# 15. Business Rules

Authentication only verifies identity.

Authentication never performs business operations.

Authentication never checks stock.

Authentication never manages inventory.

Authentication only grants access.

---

# 16. Future Enhancements

Future versions may include

Role Management

Permission Management

Password Reset

Email Verification

OTP Login

2FA

Audit Login History

These features should be added without changing existing authentication flow.

---

# 17. Summary

Authentication is intentionally lightweight in the POC.

Its only responsibility is to securely identify the user and protect backend APIs.

Business logic remains completely independent from authentication.

---

# End of Document