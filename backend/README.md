# MSMS Backend — Setup Guide

Medical Store Management System — Django REST Framework Backend

**Version:** 2.0 (POC)  
**Status:** ✅ Backend Complete  
**Stack:** Python 3.11 · Django 5.1 · DRF · SQLite (dev) / PostgreSQL (prod) · JWT

---

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (package manager)
- PostgreSQL 15+ *(production only — development uses SQLite)*

---

## First Time Setup

### Step 1 — Install uv

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2 — Create virtual environment

```powershell
cd D:\medical-management-system\backend
uv venv .venv --python 3.11
```

### Step 3 — Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4 — Install dependencies

```powershell
uv pip install -r requirements/development.txt
```

### Step 5 — Run migrations

```powershell
python manage.py makemigrations medicine supplier purchase inventory billing sales
python manage.py migrate
```

### Step 6 — Create superuser

```powershell
python manage.py createsuperuser
```

### Step 7 — Start server

```powershell
python manage.py runserver
```

---

## Useful URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000/api/docs/ | Swagger UI — all endpoints |
| http://localhost:8000/api/redoc/ | ReDoc |
| http://localhost:8000/admin/ | Django Admin |

---

## Running Tests

```powershell
# All tests
pytest -v

# Single module
pytest apps/medicine/tests/ -v
pytest apps/sales/tests/ -v

# With coverage
pytest --cov=apps --cov-report=term-missing
```

**Test results: 159 tests · 159 passed**

---

## Module Implementation Status

| Module | Status | Tests |
|--------|--------|-------|
| Project Setup | ✅ Done | — |
| Authentication | ✅ Done | 13 |
| Medicine | ✅ Done | 13 |
| Supplier | ✅ Done | 17 |
| Purchase | ✅ Done | 15 |
| Inventory | ✅ Done | 22 |
| Billing Session | ✅ Done | 18 |
| Sales + Checkout | ✅ Done | 20 |
| Dashboard | ✅ Done | 18 |
| Reports | ✅ Done | 23 |

---

## API Endpoints

### Authentication
```
POST   /api/v1/auth/login/
POST   /api/v1/auth/logout/
POST   /api/v1/auth/refresh/
GET    /api/v1/auth/me/
```

### Medicine
```
GET    /api/v1/medicines/
POST   /api/v1/medicines/
GET    /api/v1/medicines/{id}/
PUT    /api/v1/medicines/{id}/
PATCH  /api/v1/medicines/{id}/
DELETE /api/v1/medicines/{id}/          ← soft delete
GET    /api/v1/medicines/barcode/{barcode}/
```

### Supplier
```
GET    /api/v1/suppliers/
POST   /api/v1/suppliers/
GET    /api/v1/suppliers/{id}/
PUT    /api/v1/suppliers/{id}/
PATCH  /api/v1/suppliers/{id}/
DELETE /api/v1/suppliers/{id}/          ← soft delete
```

### Purchase
```
GET    /api/v1/purchases/
POST   /api/v1/purchases/               ← creates DRAFT
GET    /api/v1/purchases/{id}/
PATCH  /api/v1/purchases/{id}/
POST   /api/v1/purchases/{id}/finalize/ ← creates inventory
POST   /api/v1/purchases/{id}/cancel/
```

### Inventory
```
GET    /api/v1/inventory/batches/
GET    /api/v1/inventory/batches/{id}/
POST   /api/v1/inventory/batches/{id}/mark-expired/
POST   /api/v1/inventory/adjust/        ← manual adjustment
GET    /api/v1/inventory/ledger/        ← immutable stock history
GET    /api/v1/inventory/stock/{medicine_id}/
```

### Billing Session
```
POST   /api/v1/billing/sessions/
GET    /api/v1/billing/sessions/{id}/
DELETE /api/v1/billing/sessions/{id}/   ← cancel
POST   /api/v1/billing/sessions/{id}/items/
PATCH  /api/v1/billing/sessions/{id}/items/{item_id}/
DELETE /api/v1/billing/sessions/{id}/items/{item_id}/
```

### Sales
```
POST   /api/v1/sales/checkout/          ← converts session to sale
GET    /api/v1/sales/
GET    /api/v1/sales/{id}/
GET    /api/v1/sales/invoice/{invoice_number}/
POST   /api/v1/sales/{id}/cancel/
```

### Dashboard *(read-only)*
```
GET    /api/v1/dashboard/
GET    /api/v1/dashboard/sales/
GET    /api/v1/dashboard/purchases/
GET    /api/v1/dashboard/inventory/
GET    /api/v1/dashboard/alerts/
```

### Reports *(read-only, paginated)*
```
GET    /api/v1/reports/sales/
GET    /api/v1/reports/purchases/
GET    /api/v1/reports/inventory/
GET    /api/v1/reports/ledger/
GET    /api/v1/reports/expiry/
GET    /api/v1/reports/low-stock/
GET    /api/v1/reports/adjustments/
GET    /api/v1/reports/medicines/
GET    /api/v1/reports/suppliers/
```

---

## Project Structure

```
backend/
├── apps/
│   ├── authentication/     ← JWT login/logout/refresh
│   ├── medicine/           ← Medicine master catalog
│   ├── supplier/           ← Supplier management
│   ├── purchase/           ← Purchase → inventory trigger
│   ├── inventory/          ← InventoryBatch + Ledger (FEFO)
│   ├── billing/            ← Temporary cart before checkout
│   ├── sales/              ← Checkout → sale → invoice
│   ├── dashboard/          ← KPIs + alerts (read-only)
│   └── reports/            ← Historical reports (read-only)
├── common/
│   ├── exceptions/         ← Custom exception handler
│   ├── responses/          ← Standard response format
│   ├── pagination/         ← StandardPagination (20/page)
│   ├── permissions/
│   └── mixins/             ← BaseModel (UUID + timestamps)
├── config/
│   └── settings/
│       ├── base.py
│       ├── development.py  ← SQLite
│       └── production.py   ← PostgreSQL
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── pyproject.toml
├── pytest.ini
├── manage.py
└── .env
```

---

## Architecture Rules

1. **Views** — only receive request, call service, return response. No logic.
2. **Services** — all business logic lives here.
3. **Selectors** — read-only DB queries only.
4. **Inventory** — only `InventoryService` may modify stock. Never direct.
5. **Ledger** — immutable. Never updated or deleted.
6. **Stock** — never goes negative. FEFO always applied.
7. **Transactions** — Purchase finalize, Sale checkout are fully atomic.

---

## Environment Variables (.env)

```
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.settings.development
DEBUG=True
DB_NAME=msms_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

> For production, switch `development.py` database config to PostgreSQL.
