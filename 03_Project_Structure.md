# Project Structure

Version : 2.0

Project : Medical Store Management System (MSMS)

---

# 1. Purpose

This document defines the standard folder structure for the backend.

Every developer working on this project must follow this structure.

The objective is to keep the project:

- Clean
- Organized
- Easy to Scale
- Easy to Maintain
- Easy to Debug

---

# 2. Design Philosophy

Every folder should have only one responsibility.

No folder should become a dumping place.

The project should remain understandable even after several years of development.

---

# 3. Root Structure

backend/

    apps/

    config/

    common/

    media/

    static/

    logs/

    scripts/

    requirements/

    manage.py

---

# 4. apps/

This folder contains all business modules.

apps/

    authentication/

    medicine/

    supplier/

    purchase/

    inventory/

    sales/

    invoice/

    dashboard/

    reports/

Every business domain gets its own app.

Apps should never become dependent on unrelated apps.

---

# 5. config/

Contains project level configuration.

config/

    settings/

        base.py

        development.py

        production.py

    urls.py

    wsgi.py

    asgi.py

Environment-specific settings must remain separated.

---

# 6. common/

Contains reusable code shared across all modules.

common/

    exceptions/

    permissions/

    pagination/

    responses/

    validators/

    constants/

    mixins/

    middleware/

    utilities/

Nothing inside common should depend on a business module.

---

# 7. Standard App Structure

Example

medicine/

    admin.py

    apps.py

    urls.py

    models.py

    serializers.py

    views.py

    permissions.py

    filters.py

    services/

    validators/

    selectors/

    exceptions.py

    constants.py

    tests/

Every business app should follow the same structure.

---

# 8. services/

This folder contains business logic.

Example

services/

    medicine_service.py

    barcode_service.py

Example responsibilities

✔ Create Medicine

✔ Update Medicine

✔ Barcode Lookup

✔ Search Medicine

Views should call services.

Services should never call views.

---

# 9. selectors/

Purpose

Read-only database operations.

Example

selectors/

    medicine_selector.py

Responsibilities

Get Medicine By Barcode

Get Low Stock Medicines

Get Expiring Medicines

Get Medicine Details

Selectors should never update data.

Selectors only read data.

---

# 10. validators/

Contains business validations.

Example

validators/

    medicine_validator.py

Responsibilities

Validate Barcode

Validate Purchase Quantity

Validate Expiry

Validate MRP

Validators should never save data.

---

# 11. filters.py

Used only for searching and filtering.

Example

Medicine Search

Company Search

Category Search

Low Stock Filter

Expiry Filter

---

# 12. permissions.py

Contains API permissions.

Example

Admin Only

Cashier Access

Read Only APIs

POC version contains only basic permissions.

---

# 13. constants.py

Store fixed values.

Example

Minimum Stock

Medicine Status

Invoice Status

Adjustment Reasons

Never hardcode strings repeatedly.

---

# 14. exceptions.py

Contains custom exceptions.

Example

MedicineNotFound

OutOfStock

InvalidPurchase

DuplicateBarcode

Never raise generic exceptions when a custom one is more meaningful.

---

# 15. tests/

Each app contains its own tests.

Example

tests/

    test_models.py

    test_services.py

    test_api.py

Business logic should always be tested.

---

# 16. logs/

Contains application logs.

Examples

Application Errors

Inventory Changes

System Logs

Logs should never be stored inside business apps.

---

# 17. media/

Stores uploaded files.

Future

Medicine Images

Invoices

Supplier Documents

Temporary Files

---

# 18. static/

Stores static assets.

Mostly unused in API projects.

Reserved for future requirements.

---

# 19. scripts/

Contains helper scripts.

Examples

Seed Medicines

Create Admin

Import Data

Cleanup Database

Never mix utility scripts with application code.

---

# 20. requirements/

Contains dependency files.

requirements/

    base.txt

    development.txt

    production.txt

Never install unnecessary packages in production.

---

# 21. App Communication Rules

Example

Purchase Module

↓

Inventory Service

↓

Inventory Updated

Correct

Purchase

↓

Inventory Service

Wrong

Purchase

↓

Medicine Model

↓

Stock Updated

Always communicate through services.

---

# 22. Import Rules

Allowed

View

↓

Service

↓

Selector

↓

Model

Not Allowed

Model

↓

View

Not Allowed

Serializer

↓

View

Avoid circular imports.

---

# 23. Dependency Flow

View

↓

Serializer

↓

Validator

↓

Service

↓

Selector

↓

Model

↓

Database

This flow should never be reversed.

---

# 24. Naming Rules

App

medicine

File

medicine_service.py

Class

MedicineService

Function

create_medicine()

Variable

purchase_price

Constant

LOW_STOCK_LIMIT

Follow naming conventions consistently.

---

# 25. Future Expansion

Future modules can be added without modifying existing structure.

Examples

notification/

analytics/

ocr/

ai/

whatsapp/

barcode_printer/

thermal_printer/

Every new feature should become an independent module.

---

# 26. Summary

This project structure ensures:

✔ Small apps

✔ Reusable code

✔ Clean services

✔ Organized business logic

✔ Easy maintenance

✔ Better testing

✔ Scalable architecture

Following this structure throughout the project will significantly reduce future technical debt.

---

# End of Document