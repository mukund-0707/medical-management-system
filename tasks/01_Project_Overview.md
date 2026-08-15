# Medical Store Management System (MSMS)

**Version:** 2.0 (POC)  
**Status:** Planning  
**Author:** Mukund

---

# 1. Project Overview

Medical Store Management System (MSMS) is a backend-first application developed to simplify and automate the day-to-day operations of a medical store.

The system focuses on maintaining accurate inventory, fast billing, purchase tracking, stock movement, and reporting while minimizing manual work.

Unlike traditional inventory systems where stock is directly edited, this system follows an **Inventory-Driven Architecture**, where every stock movement is generated through a business operation and recorded in history.

The goal of this project is to build a production-quality backend that can later evolve into a complete ERP or SaaS platform without major architectural changes.

---

# 2. Project Objectives

The primary objectives are:

- Manage medicine inventory.
- Eliminate manual stock calculation.
- Support barcode-based billing.
- Automatically update inventory after every purchase and sale.
- Track every stock movement.
- Generate reports.
- Provide dashboard analytics.
- Maintain complete inventory history.

The owner should always know:

- Current stock
- Available stock
- Low stock medicines
- Expired medicines
- Purchase history
- Sales history

without performing any manual calculations.

---

# 3. POC Scope

This version is a Proof of Concept (POC).

The goal is to validate the complete business workflow of a single medical store.

### Included Modules

- Authentication
- Medicine Master
- Supplier Management
- Purchase Management
- Inventory Management
- Barcode Billing
- Sales Management
- Invoice Management
- Dashboard
- Reports

### Excluded Modules

The following features are intentionally excluded from Version 1.

- User Management
- Role Management
- Permission Management
- Multi Store Support
- OCR Invoice Reading
- AI Features
- Voice Commands
- WhatsApp Integration
- Email Notifications
- Cloud Deployment
- Mobile Application

These features will be added only after the core system becomes stable.

---

# 4. Target Users

The POC supports only two users.

## Admin

Responsible for:

- Medicine Management
- Supplier Management
- Purchase Entry
- Inventory Verification
- Manual Stock Adjustment
- Dashboard
- Reports

---

## Cashier

Responsible for:

- Barcode Billing
- Medicine Search
- Sales
- Invoice Generation

No advanced permission management is required in this version.

---

# 5. Core Philosophy

This project follows one important principle.

> **Inventory is the heart of the system.**

Every module either increases inventory, decreases inventory, or reads inventory.

Everything revolves around inventory.

---

# 6. Business Workflow

Supplier

↓

Purchase

↓

Inventory Increase

↓

Medicine Available

↓

Barcode Scan

↓

Sale

↓

Inventory Decrease

↓

Invoice

↓

Dashboard

↓

Reports

Every operation automatically updates inventory.

---

# 7. Inventory Philosophy

Inventory should never be treated as a simple number.

Instead, inventory is a result of business operations.

Example

Purchase

+100

↓

Sale

-5

↓

Damage

-2

↓

Customer Return

+1

↓

Final Stock

94

The system calculates inventory through controlled business operations.

---

# 8. Manual Inventory Adjustment

Although inventory is managed automatically, there are situations where manual correction becomes necessary.

Examples:

- Physical stock mismatch
- Damaged medicines
- Lost medicines
- Wrong purchase quantity
- Supplier correction
- Expired medicines

For this reason, the system provides an **Inventory Adjustment** feature.

Important:

Manual adjustment is **not** a silent database overwrite. The stock in the database **will definitely be updated** to reflect the correct quantity, but it cannot bypass history.

Every adjustment must:

- Record previous quantity
- Record new quantity
- Store adjustment reason
- Record adjustment date
- Record adjusted by
- Create stock ledger entry

This ensures complete traceability.

---

# 9. Stock Ledger Philosophy

Every inventory movement must create a ledger record.

Examples:

Purchase

+100

Sale

-2

Damage

-1

Adjustment

+5

Customer Return

+2

The ledger becomes the complete history of inventory.

Stock should never change without creating a ledger entry.

---

# 10. Barcode Philosophy

Barcode scanner is only an input device.

It does not know:

- Medicine Name
- Price
- Stock
- Batch
- Expiry

It simply sends the barcode number.

Example

8904043901234

↓

Backend

↓

Medicine Lookup

↓

Medicine Found

↓

Billing

↓

Inventory Update

The backend is fully responsible for identifying the medicine.

---

# 11. High Level Modules

The backend consists of the following modules.

- Authentication
- Medicine
- Supplier
- Purchase
- Inventory
- Barcode
- Sales
- Invoice
- Dashboard
- Reports
- Common Utilities

Every module should remain independent and loosely coupled.

---

# 12. Development Principles

The project follows these principles.

### Principle 1

Never update stock directly.

Always use inventory services.

---

### Principle 2

Never place business logic inside Views.

Views only receive requests and return responses.

---

### Principle 3

Never trust frontend calculations.

Everything is validated by the backend.

---

### Principle 4

Every stock movement must create a history.

---

### Principle 5

Every important operation should be transactional.

Either everything succeeds or nothing is saved.

---

# 13. Technology Stack

Backend

- Python
- Django
- Django REST Framework

Database

- PostgreSQL

Authentication

- JWT

Documentation

- Swagger / OpenAPI

Development

- Git
- Docker (Future)

---

# 14. Project Success Criteria

The Proof of Concept will be considered successful when the following workflow operates correctly.

Login

↓

Create Medicine

↓

Purchase Medicine

↓

Inventory Increased

↓

Barcode Scan

↓

Generate Sale

↓

Inventory Reduced

↓

Invoice Generated

↓

Dashboard Updated

↓

Reports Updated

↓

Stock Ledger Updated

If this complete workflow functions correctly without manual stock calculation, the backend architecture is considered validated.

---

# 15. Future Expansion

The architecture should support future enhancements without redesign.

Future features include:

- Multi Store
- AI
- OCR
- WhatsApp Billing
- Mobile App
- Cloud Deployment
- Analytics
- Redis
- Celery
- Barcode Printer
- Thermal Printer

The backend should remain modular so these features can be integrated independently.

---

# End of Document