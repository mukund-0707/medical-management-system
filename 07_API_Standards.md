# API Standards

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : High

---

# 1. Purpose

This document defines the API development standards for the Medical Store Management System.

Every API developed in this project must follow these standards.

The objective is to keep all APIs

- Consistent
- Predictable
- Easy to Maintain
- Easy to Integrate
- Easy to Debug

No API should be developed outside these standards.

---

# 2. API Style

The project follows REST API architecture.

Every endpoint should represent a business resource.

Examples

/api/medicines/

/api/purchases/

/api/sales/

/api/suppliers/

Avoid RPC style APIs whenever possible.

Wrong

/createPurchase

/getMedicine

/updateMedicine

Correct

POST /api/purchases/

GET /api/medicines/

PUT /api/medicines/{id}/

DELETE /api/medicines/{id}/

---

# 3. API Versioning

Every endpoint must contain version information.

Example

/api/v1/medicines/

/api/v1/purchases/

/api/v1/sales/

Future versions

/api/v2/

This avoids breaking old clients.

---

# 4. HTTP Methods

GET

Read data

POST

Create data

PUT

Full Update

PATCH

Partial Update

DELETE

Soft Delete (Never permanently delete business data)

---

# 5. URL Naming Rules

Use plural nouns.

Correct

/api/v1/medicines/

/api/v1/purchases/

/api/v1/suppliers/

/api/v1/sales/

Wrong

/api/v1/medicine/

/api/v1/getMedicine

/api/v1/addPurchase

URLs should never contain verbs.

---

# 6. Standard Success Response

Every successful API should return the same structure.

{
    "success": true,
    "message": "Medicine created successfully.",
    "data": {}
}

This structure should be used consistently.

---

# 7. Standard Error Response

Every failed request should return

{
    "success": false,
    "message": "Validation failed.",
    "errors": {
        "field": [
            "Reason"
        ]
    }
}

Never return raw Python exceptions.

Never expose internal errors.

---

# 8. HTTP Status Codes

200

Success

201

Created

204

Deleted Successfully

400

Validation Error

401

Authentication Failed

403

Permission Denied

404

Not Found

409

Conflict

422

Business Rule Failed

500

Unexpected Server Error

---

# 9. Authentication

JWT Authentication

Login

↓

Access Token

↓

Protected APIs

↓

Authorization Header

Public APIs

Only Login API

Every other API requires authentication.

---

# 10. Pagination

Every list API must support pagination.

Example

GET

/api/v1/medicines/?page=1&page_size=20

Default Page Size

20

Maximum

100

Never return thousands of records at once.

---

# 11. Searching

Supported using

search

Example

/api/v1/medicines/?search=dolo

Search should work on

Medicine Name

Generic Name

Barcode

Company

---

# 12. Filtering

Supported using query parameters.

Examples

Status

Category

Supplier

Low Stock

Expiry

Examples

/api/v1/medicines/?status=active

/api/v1/purchases/?supplier=1

/api/v1/sales/?date=2026-08-01

---

# 13. Sorting

Support

ordering

Example

/api/v1/medicines/?ordering=name

/api/v1/medicines/?ordering=-created_at

Ascending

field

Descending

-field

---

# 14. Soft Delete

Business data should never be permanently deleted.

Instead

Status

↓

Inactive

Deleted records remain available for history.

Inventory Ledger is never deleted.

---

# 15. Validation Rules

Backend validates everything.

Examples

Medicine Exists

Supplier Exists

Barcode Exists

Stock Available

Batch Exists

Quantity > 0

Expiry Valid

Never trust frontend validation.

---

# 16. Business Rule Errors

Example

Out Of Stock

{
    "success": false,
    "message": "Requested quantity exceeds available stock."
}

Duplicate Barcode

{
    "success": false,
    "message": "Barcode already exists."
}

Medicine Not Found

{
    "success": false,
    "message": "Medicine not found."
}

Business errors should be readable.

---

# 17. API Transactions

Critical APIs should always use database transactions.

Examples

Purchase

Sale

Inventory Adjustment

Customer Return

Supplier Return

If any operation fails

Rollback Everything

---

# 18. Logging

Every critical API should generate logs.

Examples

Purchase Created

Medicine Updated

Inventory Adjusted

Sale Completed

Invoice Printed

Logs are for debugging and auditing.

---

# 19. Performance Guidelines

Always use

select_related()

prefetch_related()

bulk_create()

bulk_update()

Indexes

barcode

batch_number

invoice_number

Avoid unnecessary queries.

---

# 20. API Security

Every request must

Validate Token

Validate Input

Validate Business Rules

Prevent Negative Stock

Prevent Duplicate Barcode

Reject Invalid Batch

Never expose database IDs unnecessarily in URLs if UUIDs are used.

---

# 21. API Documentation

Every endpoint must be documented.

Swagger/OpenAPI should include

Purpose

Request

Response

Validation Rules

Possible Errors

Authentication

Example Request

Example Response

No undocumented API should exist.

---

# 22. Standard Endpoint Naming

Authentication

POST   /api/v1/auth/login/

Medicine

GET    /api/v1/medicines/

POST   /api/v1/medicines/

PUT    /api/v1/medicines/{id}/

PATCH  /api/v1/medicines/{id}/

DELETE /api/v1/medicines/{id}/

Supplier

GET    /api/v1/suppliers/

POST   /api/v1/suppliers/

Purchase

GET    /api/v1/purchases/

POST   /api/v1/purchases/

Sales

GET    /api/v1/sales/

POST   /api/v1/sales/

Reports

GET    /api/v1/reports/

Dashboard

GET    /api/v1/dashboard/

---

# 23. Architect Decisions

Accepted

✔ REST API

✔ JWT Authentication

✔ Standard Response Format

✔ Standard Error Format

✔ Pagination

✔ Search

✔ Filtering

✔ Soft Delete

✔ Transaction-based Operations

Rejected

✘ Random API Structure

✘ Different Response Formats

✘ Business Logic inside Views

✘ Frontend Calculations

✘ Permanent Delete for Business Data

---

# 24. Summary

Every API in the Medical Store Management System must follow one consistent standard.

Following these standards ensures

- Predictable APIs
- Easier Frontend Integration
- Better Debugging
- Cleaner Code
- Faster Development
- Easier Future Maintenance

These standards are mandatory for every module.

---

# End of Document