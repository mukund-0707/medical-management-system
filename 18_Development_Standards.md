# Development Standards

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Mandatory

---

# 1. Purpose

This document defines the software engineering standards for the Medical Store Management System.

Every developer contributing to the project must follow these standards.

The objective is to ensure

- Consistent code quality
- Maintainable architecture
- Predictable APIs
- Reliable inventory management
- Easier debugging
- Easier onboarding of new developers

These standards are mandatory.

---

# 2. General Development Principles

The project follows the following principles.

- Single Responsibility Principle (SRP)
- Don't Repeat Yourself (DRY)
- Keep It Simple (KISS)
- Explicit is better than implicit
- Business logic belongs to Services
- Database is the source of truth
- Inventory is the owner of stock

Never compromise these principles.

---

# 3. Project Structure Standards

Every business module must follow the same structure.

apps/

    medicine/

        models.py

        serializers.py

        views.py

        urls.py

        admin.py

        filters.py

        permissions.py

        constants.py

        exceptions.py

        selectors/

        validators/

        services/

        tests/

Business logic should never be placed in Views or Models.

---

# 4. Naming Conventions

Apps

medicine

supplier

purchase

inventory

sales

reports

Files

medicine_service.py

inventory_service.py

Classes

MedicineService

InventoryService

PurchaseValidator

InventorySelector

Functions

create_purchase()

reduce_inventory()

validate_batch()

Variables

medicine_name

purchase_price

available_quantity

Constants

LOW_STOCK_LIMIT

DEFAULT_PAGE_SIZE

INVENTORY_MOVEMENT_TYPES

Enums

InventoryStatus

PaymentMode

AdjustmentReason

---

# 5. Service Layer Standards

Every business operation must pass through Services.

Example

View

↓

Serializer

↓

Service

↓

Selector

↓

Model

Services are responsible for

Business Logic

Transactions

Calling Other Modules

Validation Orchestration

Services must never

Return HTTP Responses

Access Request Objects

Perform Serialization

---

# 6. Selector Standards

Selectors are read-only.

Responsibilities

Database Queries

Search

Filtering

Aggregation

Selectors never

Update Data

Delete Data

Create Data

---

# 7. Validator Standards

Validators are responsible only for business validation.

Example

Validate Stock

Validate Batch

Validate Supplier

Validate Barcode

Validators never save data.

---

# 8. Model Standards

Models represent database schema only.

Models should not contain business workflows.

Allowed

Properties

Simple helper methods

Not Allowed

Inventory calculation

Purchase processing

Sale processing

Invoice generation

---

# 9. View Standards

Views should remain lightweight.

View Responsibilities

Authentication

Authorization

Serializer

Calling Services

Returning Response

Views must never

Calculate totals

Reduce inventory

Create ledger entries

Run business workflows

---

# 10. Serializer Standards

Serializers validate request and response data.

Serializers must never

Update stock

Create ledger

Generate invoice

Perform business calculations

---

# 11. API Standards

Every endpoint follows REST.

GET

Read

POST

Create

PUT

Full Update

PATCH

Partial Update

DELETE

Soft Delete

Versioning

/api/v1/

Every API returns standard response format.

---

# 12. Database Standards

Primary Keys

UUID

Foreign Keys

Always enforced

Indexes

Barcode

Medicine

Batch

Invoice Number

Sale Date

Purchase Date

Never use raw SQL unless absolutely necessary.

---

# 13. Inventory Standards

Inventory can only be modified by Inventory Service.

Never update stock directly.

Wrong

medicine.stock = 100

Correct

InventoryService.adjust_stock(...)

Every inventory movement creates a ledger entry.

Negative stock is prohibited.

FEFO must always be followed.

---

# 14. Transaction Standards

The following operations must execute inside database transactions.

Purchase Finalization

Checkout

Inventory Adjustment

Customer Return

Supplier Return

If any step fails

Rollback everything.

Partial updates are forbidden.

---

# 15. Logging Standards

Every important business event must generate logs.

Medicine Created

Purchase Finalized

Sale Completed

Inventory Adjustment

Customer Return

Supplier Return

Login Failed

Unexpected Errors

Logs should contain

Timestamp

User

Module

Action

Reference ID

Severity

---

# 16. Error Handling Standards

Never expose internal exceptions.

Never return stack traces.

Convert all exceptions into standard API responses.

Unexpected exceptions should be logged.

Expected business exceptions should return meaningful messages.

---

# 17. Exception Categories

Validation Error

Invalid request data.

Authentication Error

Invalid or expired token.

Authorization Error

Permission denied.

Business Rule Error

Business constraint violation.

Database Error

Unexpected persistence issue.

System Error

Unhandled server error.

---

# 18. Standard Error Response

{
    "success": false,
    "message": "Requested quantity exceeds available stock.",
    "errors": {}
}

Never expose

Python tracebacks

SQL statements

Internal server details

---

# 19. Business Exceptions

Examples

MedicineNotFound

SupplierNotFound

OutOfStock

DuplicateBarcode

InvalidBatch

ExpiredMedicine

InactiveMedicine

DuplicateInvoice

Business exceptions should be descriptive.

---

# 20. Logging Policy

INFO

Successful business operations.

WARNING

Business rule violations.

ERROR

Unexpected failures.

CRITICAL

System failure causing application instability.

All critical errors must include stack trace in server logs.

Stack traces must never be returned to clients.

---

# 21. Testing Philosophy

Every business module must be testable.

Testing is mandatory.

No critical feature should be merged without tests.

---

# 22. Unit Tests

Unit tests verify

Services

Validators

Selectors

Utility Functions

Every business rule should have unit tests.

---

# 23. Integration Tests

Integration tests verify

Purchase

Inventory

Sales

Ledger

Authentication

Database Transactions

Integration tests ensure modules work together correctly.

---

# 24. API Tests

Test

Success

Validation Failure

Authentication Failure

Permission Failure

Business Rule Failure

Unexpected Error

Every public API should be covered.

---

# 25. Inventory Tests

Mandatory scenarios

Purchase increases stock

Sale decreases stock

FEFO allocation

Multi-batch sale

Inventory adjustment

Damage

Expiry

Purchase return

Customer return

Negative stock rejection

These tests are critical.

---

# 26. Transaction Tests

Verify rollback scenarios.

Inventory creation failure

↓

Purchase rollback

Ledger failure

↓

Sale rollback

Database failure

↓

Rollback everything

No partial data should remain.

---

# 27. Performance Tests

Verify

Barcode lookup

Medicine search

Dashboard loading

Large inventory

Large sales history

Large ledger

The application should remain responsive with large datasets.

---

# 28. Security Standards

JWT Authentication

Input Validation

Parameterized ORM Queries

No hardcoded secrets

Environment variables only

CSRF disabled only where appropriate for JWT APIs

Validate all user input

---

# 29. Documentation Standards

Every module must contain

Purpose

Responsibilities

Workflow

Business Rules

Edge Cases

API Endpoints

Future Scope

Every public API must appear in Swagger/OpenAPI.

---

# 30. Code Review Checklist

Before merging any feature

✔ Code follows architecture

✔ Tests pass

✔ No direct stock update

✔ Transaction safety verified

✔ Logging added

✔ Validation complete

✔ No duplicate logic

✔ API documented

✔ Performance reviewed

✔ Edge cases covered

---

# 31. Architect Rules

Rule 1

Inventory owns stock.

Rule 2

Ledger owns history.

Rule 3

Medicine owns identity.

Rule 4

Purchase creates inventory.

Rule 5

Sales consume inventory.

Rule 6

Reports never modify data.

Rule 7

Dashboard is read-only.

Rule 8

Business logic belongs only in Services.

Rule 9

Every stock movement is traceable.

Rule 10

Every critical operation is transactional.

---

# 32. Definition of Done (DoD)

A feature is considered complete only if

✔ Business workflow implemented

✔ Validation complete

✔ Unit tests written

✔ Integration tests pass

✔ API documented

✔ Logging implemented

✔ Transaction safe

✔ Error handling implemented

✔ Edge cases handled

✔ Code reviewed

Only then is a feature ready for production.

---

# End of Document