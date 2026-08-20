# Backend Changes & API Reference — MSMS

## Audit Summary

Poora backend audit kiya gaya. Backend **production-ready quality** mein hai.
Sirf ek cheez missing thi — CORS configuration (React frontend ke liye).

---

## Changes Made

### 1. CORS Configuration Fix

**Problem:** `corsheaders` package `requirements/base.txt` mein tha, lekin:
- `INSTALLED_APPS` mein add nahi kiya tha
- `MIDDLEWARE` mein `CorsMiddleware` nahi tha
- `development.py` mein `CORS_ALLOW_ALL_ORIGINS` commented out tha

**Files Changed:**

#### `backend/config/settings/base.py`
```python
# INSTALLED_APPS mein add kiya:
THIRD_PARTY_APPS = [
    'corsheaders',   # ← ADDED
    'rest_framework',
    ...
]

# MIDDLEWARE mein sabse upar add kiya (required by django-cors-headers):
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # ← ADDED (must be first)
    'django.middleware.security.SecurityMiddleware',
    ...
]
```

#### `backend/config/settings/development.py`
```python
# Uncomment aur enable kiya:
CORS_ALLOW_ALL_ORIGINS = True   # ← ENABLED
CORS_ALLOW_CREDENTIALS = True   # ← ADDED
```

---

## Backend Status — What Works

### Authentication
- ✅ Django default `auth.User` use karta hai (`createsuperuser` compatible)
- ✅ JWT tokens (SimpleJWT) — access + refresh
- ✅ Token blacklisting on logout
- ✅ Token rotation on refresh

### All Modules — CRUD Status
| Module     | List | Create | Read | Update | Delete | Extra |
|------------|------|--------|------|--------|--------|-------|
| Medicine   | ✅   | ✅     | ✅   | ✅     | ✅ (soft) | Barcode lookup |
| Supplier   | ✅   | ✅     | ✅   | ✅     | ✅ (soft) | — |
| Purchase   | ✅   | ✅     | ✅   | ✅ (draft only) | — | Finalize, Cancel |
| Inventory  | ✅   | —      | ✅   | —      | — | Adjust stock, Mark expired, Ledger |
| Billing    | ✅   | ✅     | ✅   | ✅     | ✅ | Add/remove items from cart |
| Sales      | ✅   | —      | ✅   | —      | ✅ (cancel) | Checkout, Invoice lookup |
| Dashboard  | ✅   | —      | —    | —      | — | KPI, Alerts, Sales/Purchase/Inventory summary |
| Reports    | ✅   | —      | —    | —      | — | Sales, Purchase, Inventory, Expiry, Low Stock, Ledger |

---

## API Endpoints Reference

### Base URL
```
http://127.0.0.1:8000/api/v1/
```

### Swagger Docs
```
http://127.0.0.1:8000/api/docs/
```

---

### Authentication — `/api/v1/auth/`

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/v1/auth/login/` | ❌ | Login — returns JWT tokens |
| POST | `/api/v1/auth/logout/` | ✅ | Logout — blacklists refresh token |
| POST | `/api/v1/auth/refresh/` | ❌ | Get new access token |
| GET  | `/api/v1/auth/me/` | ✅ | Current user info |

**Login Request:**
```json
POST /api/v1/auth/login/
{
  "username": "admin",
  "password": "your_password"
}
```

**Login Response:**
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "access": "eyJ...",
    "refresh": "eyJ...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "first_name": "",
      "last_name": "",
      "is_staff": true
    }
  }
}
```

**All protected endpoints mein header lagao:**
```
Authorization: Bearer <access_token>
```

---

### Medicine — `/api/v1/medicines/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/medicines/` | List all medicines (paginated) |
| POST   | `/api/v1/medicines/` | Create medicine |
| GET    | `/api/v1/medicines/{uuid}/` | Get single medicine |
| PUT    | `/api/v1/medicines/{uuid}/` | Full update |
| PATCH  | `/api/v1/medicines/{uuid}/` | Partial update |
| DELETE | `/api/v1/medicines/{uuid}/` | Soft deactivate |
| GET    | `/api/v1/medicines/barcode/{barcode}/` | Barcode lookup |

**Query Params:** `search`, `status`, `category`, `ordering`, `page`, `page_size`

---

### Supplier — `/api/v1/suppliers/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/suppliers/` | List all suppliers |
| POST   | `/api/v1/suppliers/` | Create supplier |
| GET    | `/api/v1/suppliers/{uuid}/` | Get supplier |
| PUT    | `/api/v1/suppliers/{uuid}/` | Full update |
| PATCH  | `/api/v1/suppliers/{uuid}/` | Partial update |
| DELETE | `/api/v1/suppliers/{uuid}/` | Soft deactivate |

---

### Purchase — `/api/v1/purchases/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/purchases/` | List purchases |
| POST   | `/api/v1/purchases/` | Create draft PO |
| GET    | `/api/v1/purchases/{uuid}/` | Get purchase |
| PATCH  | `/api/v1/purchases/{uuid}/` | Update (draft only) |
| POST   | `/api/v1/purchases/{uuid}/finalize/` | Finalize → updates inventory |
| POST   | `/api/v1/purchases/{uuid}/cancel/` | Cancel PO |

---

### Inventory — `/api/v1/inventory/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/inventory/batches/` | List all batches |
| GET    | `/api/v1/inventory/batches/{uuid}/` | Get batch |
| POST   | `/api/v1/inventory/batches/{uuid}/mark-expired/` | Mark batch expired |
| POST   | `/api/v1/inventory/adjust/` | Manual stock adjustment |
| GET    | `/api/v1/inventory/ledger/` | Stock movement history |
| GET    | `/api/v1/inventory/stock/{medicine_uuid}/` | Stock summary for medicine |

---

### Billing — `/api/v1/billing/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/v1/billing/sessions/` | Create billing session (cart) |
| GET    | `/api/v1/billing/sessions/{uuid}/` | Get session with items |
| DELETE | `/api/v1/billing/sessions/{uuid}/` | Cancel session |
| POST   | `/api/v1/billing/sessions/{uuid}/items/` | Add item to cart |
| PATCH  | `/api/v1/billing/sessions/{uuid}/items/{item_uuid}/` | Update cart item |
| DELETE | `/api/v1/billing/sessions/{uuid}/items/{item_uuid}/` | Remove item |

---

### Sales — `/api/v1/sales/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/sales/` | List all sales |
| GET    | `/api/v1/sales/{uuid}/` | Get sale details |
| POST   | `/api/v1/sales/checkout/` | Checkout billing session → creates sale |
| POST   | `/api/v1/sales/{uuid}/cancel/` | Cancel sale |
| GET    | `/api/v1/sales/invoice/{invoice_number}/` | Get by invoice number |

**Checkout Request:**
```json
POST /api/v1/sales/checkout/
{
  "session_id": "uuid-of-billing-session",
  "payment_mode": "cash",  // cash, upi, card, bank_transfer
  "remarks": ""
}
```

---

### Dashboard — `/api/v1/dashboard/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/dashboard/` | KPI summary (today's stats) |
| GET    | `/api/v1/dashboard/sales/` | Sales summary |
| GET    | `/api/v1/dashboard/purchases/` | Purchase summary |
| GET    | `/api/v1/dashboard/inventory/` | Inventory health |
| GET    | `/api/v1/dashboard/alerts/` | Low stock + expiry alerts |

---

### Reports — `/api/v1/reports/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/reports/sales/` | Sales report |
| GET    | `/api/v1/reports/purchases/` | Purchase report |
| GET    | `/api/v1/reports/inventory/` | Inventory report |
| GET    | `/api/v1/reports/ledger/` | Stock ledger |
| GET    | `/api/v1/reports/expiry/` | Expiry report |
| GET    | `/api/v1/reports/low-stock/` | Low stock report |
| GET    | `/api/v1/reports/adjustments/` | Adjustment history |
| GET    | `/api/v1/reports/medicines/` | Medicine report |
| GET    | `/api/v1/reports/suppliers/` | Supplier report |

---

## How to Run Backend

```bash
cd backend

# 1. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements/development.txt

# 3. Create .env file
cp .env.example .env

# 4. Create logs directory
mkdir -p logs && touch logs/msms.log
mkdir -p static

# 5. Run migrations
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py migrate

# 6. Create superuser (for login)
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py createsuperuser

# 7. Start server
DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver
```

**Backend:** `http://127.0.0.1:8000/`
**API Docs:** `http://127.0.0.1:8000/api/docs/`

---

## Frontend Wiring Notes

Frontend ko backend se connect karne ke liye:

1. **Login** — `POST /api/v1/auth/login/` se JWT token lena
2. **Token store** — localStorage ya sessionStorage mein `access` token save karo
3. **API calls** — har request mein `Authorization: Bearer <token>` header lagao
4. **Token expire** — 8 hours mein expire hota hai, `POST /api/v1/auth/refresh/` se renew karo

**API Base URL (dev):** `http://127.0.0.1:8000/api/v1`

---

## Design Decisions

- **auth.User** — Django ka default User model use kiya (createsuperuser compatible). Custom user model future use ke liye commented out hai.
- **Soft delete** — Medicine aur Supplier delete hote nahi, sirf `is_active=False` hota hai
- **Inventory flow** — Purchase finalize hone par inventory batches bante hain (FEFO — First Expiry First Out)
- **Billing flow** — Cart (BillingSession) → Checkout → Sale + Inventory deduction
- **JWT** — Access token 8 hours, Refresh token 7 days
- **Pagination** — Default 20 items per page, max 100
