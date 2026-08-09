# System Architecture

Version : 2.0

Project : Medical Store Management System (MSMS)

---

# 1. Purpose

This document defines the complete backend architecture of the Medical Store Management System.

The objective of this architecture is to keep the backend:

- Modular
- Scalable
- Maintainable
- Testable
- Easy to Extend

Every future module must follow this architecture.

No developer should implement business logic outside this architecture.

---

# 2. Design Philosophy

The backend is designed using a modular architecture.

Each business module is responsible for only one domain.

Example

Medicine Module

↓

Responsible only for medicines.

Purchase Module

↓

Responsible only for purchases.

Sales Module

↓

Responsible only for sales.

Inventory Module

↓

Responsible only for inventory.

No module should perform another module's responsibility.

---

# 3. System Architecture

                  React Frontend

                         │

                    REST API

                         │

                  Authentication

                         │

                    Django Views

                         │

                  Request Validation

                         │

                  Business Services

                         │

                Database Operations

                         │

                   PostgreSQL

                         │

                  Response Builder

                         │

                     JSON Response

---

# 4. Backend Layers

The backend consists of multiple logical layers.

Client Layer

↓

API Layer

↓

Validation Layer

↓

Business Layer

↓

Persistence Layer

↓

Database

Each layer has its own responsibility.

---

# 5. Client Layer

Responsible for:

- Sending Requests
- Receiving Responses
- Displaying Data

Technology

React

No business calculation should happen here.

---

# 6. API Layer

Files

views.py

urls.py

Responsibilities

- Receive Request
- Authenticate User
- Call Serializer
- Call Business Service
- Return Response

Views should remain extremely small.

Views should never:

❌ Calculate Stock

❌ Generate Invoice

❌ Update Inventory

❌ Validate Purchase Logic

---

# 7. Validation Layer

Files

serializers.py

Responsibilities

- Validate Input
- Validate Required Fields
- Validate Data Types
- Validate Request Structure

Example

Purchase Quantity

Cannot be negative.

Medicine ID

Must exist.

Supplier ID

Must exist.

Barcode

Cannot be empty.

Serializers should never perform business operations.

---

# 8. Business Layer

The Business Layer is the heart of the application.

Every important decision happens here.

Files

services/

Examples

Medicine Service

Purchase Service

Inventory Service

Sales Service

Invoice Service

Barcode Service

Dashboard Service

Report Service

Examples of responsibilities

Purchase Service

Create Purchase

↓

Inventory Service

Increase Stock

↓

Ledger Service

Create History

↓

Return Success

Views should never perform these operations.

---

# 9. Database Layer

Files

models.py

Responsibilities

- Database Models
- Relationships
- Constraints

Business logic should never be written inside models.

Models should only describe the database.

---

# 10. Module Independence

Every module should remain independent.

Example

Medicine Module

Can create medicines.

Cannot update stock.

Inventory Module

Can update stock.

Cannot create supplier.

Sales Module

Can create invoices.

Cannot directly edit medicine quantity.

Each module owns its own responsibility.

---

# 11. Communication Between Modules

Correct Flow

Sales

↓

Inventory Service

↓

Stock Updated

Wrong Flow

Sales

↓

UPDATE Medicine SET stock=...

Never update another module directly.

Always use its service.

---

# 12. Project Modules

Authentication

Medicine

Supplier

Purchase

Inventory

Barcode

Sales

Invoice

Dashboard

Reports

Common

Each module must remain isolated.

---

# 13. Standard Request Flow

Every API follows the same flow.

Request

↓

View

↓

Serializer

↓

Service

↓

Database

↓

Service

↓

Response

No shortcuts.

---

# 14. Transactions

Every critical operation must use database transactions.

Example

Purchase

↓

Create Purchase

↓

Create Purchase Items

↓

Increase Inventory

↓

Create Ledger Entry

↓

Commit

If any operation fails

↓

Rollback Everything

Never allow partial updates.

---

# 15. Exception Handling

Every exception should return a standard response.

Example

{
    "success": false,
    "message": "...",
    "errors": {}
}

Never expose internal errors.

Never return Python tracebacks.

---

# 16. Logging

Important operations must be logged.

Examples

Medicine Created

Medicine Updated

Purchase Created

Purchase Deleted

Sale Completed

Invoice Cancelled

Inventory Adjusted

Logs should help debugging.

---

# 17. Naming Conventions

Apps

medicine

supplier

purchase

inventory

sales

invoice

Classes

MedicineService

PurchaseService

InventoryService

Functions

create_purchase()

reduce_stock()

generate_invoice()

Variables

purchase_price

sale_price

available_quantity

reserved_quantity

Use snake_case for variables.

Use PascalCase for classes.

---

# 18. Coding Principles

Business logic never belongs in Views.

Business logic never belongs in Serializers.

Business logic never belongs in Models.

Business logic belongs only inside Services.

This rule is mandatory.

---

# 19. Performance Guidelines

Never fetch unnecessary data.

Use

- select_related()

- prefetch_related()

Use indexes on

- barcode

- medicine_id

- invoice_number

- batch_number

Use pagination for listing APIs.

Avoid N+1 queries.

---

# 20. Scalability

This architecture should support future features without redesign.

Examples

OCR

AI

Multiple Stores

Redis

Celery

Notifications

Cloud Storage

Thermal Printer

Barcode Printer

These should be added as new modules.

Existing modules should require minimal modification.

---

# 21. What This Architecture Solves

Without this architecture

- Large Views
- Duplicate Logic
- Difficult Testing
- Hard Maintenance
- Poor Scalability

With this architecture

- Small Modules
- Clean Business Logic
- Reusable Code
- Easier Debugging
- Better Testing
- Better Performance
- Future Ready

---

# 22. Architecture Rules (Mandatory)

Rule 1

Views never contain business logic.

---

Rule 2

Stock is never updated directly.

---

Rule 3

Every inventory movement creates a ledger entry.

---

Rule 4

Every critical operation is transactional.

---

Rule 5

Modules communicate through services.

---

Rule 6

Database is the single source of truth.

---

Rule 7

Frontend never performs business calculations.

---

# End of Document