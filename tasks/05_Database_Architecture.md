# Database Architecture

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

This document defines the database architecture of the Medical Store Management System.

The database is designed to be

- Fast
- Reliable
- Easy to Maintain
- Easy to Scale

Every module depends on this design.

Database changes after implementation should be avoided.

---

# 2. Database Philosophy

The database is designed around business operations rather than simple CRUD tables.

Instead of storing only medicine quantities, the system stores business events.

Example

Purchase

↓

Inventory Updated

↓

Ledger Created

↓

Reports Updated

Every operation leaves a permanent history.

---

# 3. Database Engine

Database

PostgreSQL

Reason

- High Performance

- ACID Transactions

- Strong Indexing

- JSON Support

- Reliable

- Production Ready

---

# 4. Core Tables

The POC requires only the following tables.

authentication

medicine

supplier

purchase

purchase_item

inventory

inventory_ledger

sale

sale_item

invoice

No additional tables should be created unless required.

---

# 5. Table Responsibilities

authentication

Stores login credentials.

medicine

Stores medicine master information.

supplier

Stores supplier information.

purchase

Purchase invoice header.

purchase_item

Medicines inside purchase invoice.

inventory

Current stock snapshot.

inventory_ledger

Every stock movement.

sale

Sale header.

sale_item

Medicines sold.

invoice

Generated invoice information.

---

# 6. Database Relationships

Medicine

↓

Purchase Item

↓

Inventory

↓

Sale Item

↓

Invoice

Supplier

↓

Purchase

Purchase

↓

Purchase Items

Sale

↓

Sale Items

Medicine is the central entity.

---

# 7. Medicine Table

Purpose

Master information.

Contains

Medicine Name

Barcode

Generic Name

Manufacturer

Category

Unit

GST

MRP

Status

Medicine table should NEVER store stock.

Medicine is only product information.

---

# 8. Supplier Table

Stores

Supplier Name

Phone

GST Number

Address

Status

No inventory information should be stored here.

---

# 9. Purchase Table

Represents purchase invoice.

Contains

Invoice Number

Supplier

Purchase Date

Invoice Total

Status

Remarks

Purchase table does not store medicines.

---

# 10. Purchase Item Table

Each row represents one purchased medicine.

Contains

Purchase

Medicine

Batch Number

Expiry Date

Purchase Price

MRP

Quantity

Every purchase item creates inventory.

---

# 11. Inventory Table

Purpose

Current inventory snapshot.

Contains

Medicine

Batch Number

Available Quantity

Damaged Quantity

Expired Quantity

Last Updated

This table exists for fast reads.

It is not the history.

---

# 12. Inventory Ledger

Purpose

Complete inventory history.

Each row represents exactly one stock movement.

Movement Types

Purchase

Sale

Adjustment

Damage

Expiry

Customer Return

Supplier Return

Every movement is permanent.

Rows are never updated.

Rows are never deleted.

---

# 13. Why Two Inventory Tables?

Inventory

Fast lookup.

Dashboard.

Billing.

Current stock.

Inventory Ledger

History.

Audit.

Reports.

Without Inventory table

Current stock would require millions of calculations.

Without Ledger

History would be lost.

Both are required.

---

# 14. Sale Table

Represents one completed sale.

Contains

Invoice Number

Sale Date

Payment Mode

Grand Total

Discount

Tax

Status

No medicine details here.

---

# 15. Sale Item Table

Contains

Sale

Medicine

Batch

Quantity

Price

Discount

GST

Total

Each sale item decreases inventory.

---

# 16. Invoice Table

Stores printable invoice information.

Contains

Invoice Number

Sale

Invoice Date

Total Amount

Invoice Status

Invoice can be regenerated anytime.

---

# 17. Primary Keys

Every table should use UUID.

Never expose sequential IDs.

Reason

Better Security

Future Sync

Easy Merge

API Friendly

---

# 18. Foreign Keys

Every relation should use Foreign Keys.

Medicine

↓

Purchase Item

Purchase

↓

Purchase Item

Sale

↓

Sale Item

Medicine

↓

Inventory

Medicine

↓

Inventory Ledger

This maintains integrity.

---

# 19. Indexing Strategy

Indexes must exist on

Barcode

Medicine Name

Batch Number

Expiry Date

Invoice Number

Purchase Date

Sale Date

Movement Type

Proper indexing is mandatory.

---

# 20. Soft Delete

Medicine

Supplier

Purchase

Sale

Should use Active / Inactive status.

Never permanently delete business data.

Inventory Ledger should NEVER be deleted.

---

# 21. Transactions

Purchase

↓

Purchase Item

↓

Inventory

↓

Ledger

↓

Commit

Failure

↓

Rollback

Same applies to Sales.

---

# 22. Data Integrity Rules

Medicine must exist before Purchase.

Medicine must exist before Sale.

Supplier must exist before Purchase.

Inventory must exist before Sale.

Stock cannot become negative.

Batch is mandatory.

Expiry is mandatory.

---

# 23. Audit Philosophy

Every important business event should remain traceable.

Questions the system should answer:

Who changed stock?

When?

Why?

Which invoice?

Which batch?

Audit information should never be lost.

---

# 24. Future Expansion

Future tables

customer

notification

analytics

ocr_import

store

warehouse

stock_transfer

purchase_order

These can be added without changing current architecture.

---

# 25. Database Summary

Medicine

↓

Purchase

↓

Inventory

↓

Sale

↓

Invoice

↓

Reports

↓

Dashboard

Inventory remains the central business component.

Database is optimized for both fast reads and complete audit history.

---

# End of Document