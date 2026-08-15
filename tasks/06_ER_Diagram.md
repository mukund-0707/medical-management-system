# Entity Relationship Diagram (ER Diagram)

Version : 2.0

Project : Medical Store Management System

---

# Purpose

This document defines the relationship between all business entities.

No database table should be created without following this design.

This ER Diagram becomes the single source of truth for database relationships.

---

# Business Entities

1. User

2. Medicine

3. Supplier

4. Purchase

5. Purchase Item

6. Inventory Batch

7. Inventory Ledger

8. Sale

9. Sale Item

---

# Relationship Diagram

                    User
                     │
                     │
      ┌──────────────┴──────────────┐
      │                             │
      │                             │
 Purchase                     Sale
      │                             │
      │                             │
 Purchase Item               Sale Item
      │                             │
      └──────────────┐──────────────┘
                     │
               Inventory Batch
                     │
                     │
             Inventory Ledger
                     │
                     │
                 Medicine
                     │
                     │
                 Supplier

---

# Medicine Relationships

Medicine

↓

Purchase Item

One Medicine

↓

Many Purchase Items

---

Medicine

↓

Inventory Batch

One Medicine

↓

Many Inventory Batches

---

Medicine

↓

Sale Item

One Medicine

↓

Many Sale Items

---

Medicine

↓

Inventory Ledger

One Medicine

↓

Many Ledger Entries

---

# Supplier Relationships

Supplier

↓

Purchase

One Supplier

↓

Many Purchases

Supplier is never directly connected with Inventory.

Inventory only changes after Purchase completion.

---

# Purchase Relationships

Purchase

↓

Purchase Item

One Purchase

↓

Many Purchase Items

Purchase cannot exist without Purchase Items.

---

# Purchase Item Relationships

Every Purchase Item creates exactly one Inventory Batch.

Purchase Item

↓

Inventory Batch

One

↓

One

Reason

Each purchase receives a unique batch.

---

# Inventory Batch Relationships

Inventory Batch

↓

Inventory Ledger

One Batch

↓

Many Ledger Entries

Example

Purchase

↓

+100

Sale

↓

-5

Damage

↓

-2

Return

↓

+3

Everything is stored in Ledger.

---

# Sale Relationships

Sale

↓

Sale Item

One Sale

↓

Many Sale Items

Sale header stores

Invoice Information

Sale Items store

Medicines.

---

# Sale Item Relationships

Sale Item

↓

Inventory Batch

Many Sale Items

↓

One Inventory Batch

Every sale always reduces a specific batch.

Never reduce stock directly from Medicine.

---

# Inventory Ledger Relationships

Inventory Ledger

↓

Inventory Batch

Many

↓

One

Ledger records every movement.

Purchase

Sale

Return

Damage

Expiry

Adjustment

Ledger is append-only.

Rows are never deleted.

Rows are never updated.

---

# Cardinality

Medicine

1

↓

N

Purchase Item

---------------------------------

Medicine

1

↓

N

Inventory Batch

---------------------------------

Medicine

1

↓

N

Sale Item

---------------------------------

Supplier

1

↓

N

Purchase

---------------------------------

Purchase

1

↓

N

Purchase Item

---------------------------------

Sale

1

↓

N

Sale Item

---------------------------------

Inventory Batch

1

↓

N

Inventory Ledger

---------------------------------

Inventory Batch

1

↓

N

Sale Item

---

# Inventory Flow

Purchase

↓

Purchase Item

↓

Inventory Batch

↓

Inventory Ledger

↓

Available Stock

↓

Sale

↓

Sale Item

↓

Inventory Ledger

↓

Updated Stock

---

# Rules

Rule 1

Medicine never stores stock.

---

Rule 2

Inventory Batch stores current quantity.

---

Rule 3

Inventory Ledger stores history.

---

Rule 4

Sale Item always references Inventory Batch.

---

Rule 5

Purchase Item always creates Inventory Batch.

---

Rule 6

Ledger is immutable.

---

Rule 7

Inventory is always batch-wise.

---

Rule 8

Reports are generated using

Inventory Batch

+

Inventory Ledger

+

Sales

+

Purchase

---

# Database Summary

Master Tables

Medicine

Supplier

User

Transaction Tables

Purchase

Purchase Item

Sale

Sale Item

Inventory Tables

Inventory Batch

Inventory Ledger

---

# Architect Decisions

Accepted

✔ Batch-wise Inventory

✔ Separate Ledger

✔ Separate Batch Table

✔ Immutable Ledger

✔ Service-based Updates

Rejected

✘ Direct Stock Column in Medicine

✘ Updating Stock without Ledger

✘ Inventory History inside Medicine

✘ Duplicate Invoice Table

Future

Warehouse

Multi Store

Stock Transfer

Reserved Stock

AI Prediction

Notification Engine

These can be added without changing current relationships.

---

# End of Document