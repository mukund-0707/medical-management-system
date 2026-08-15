# Business Workflows

Version: 2.0

Project: Medical Store Management System (MSMS)

Priority: Critical

---

# Purpose

This document defines every business workflow of the Medical Store Management System.

Every module must follow these workflows.

Business workflow always comes before implementation.

---

# System Principle

The system is Inventory Driven.

Every business operation must either

- Increase Inventory
- Decrease Inventory
- Read Inventory
- Adjust Inventory

No module should directly update stock.

---

# Workflow 1 : Add New Medicine

Admin

↓

Open Medicine Module

↓

Click Add Medicine

↓

Enter Medicine Details

↓

Save Medicine

↓

Medicine Master Updated

Important

Adding a medicine DOES NOT increase stock.

Medicine is only registered.

Stock remains ZERO.

---

# Workflow 2 : Purchase Medicine

Supplier

↓

Purchase Invoice

↓

Create Purchase

↓

Add Purchase Items

↓

Validate Data

↓

Save Purchase

↓

Create Inventory Batch

↓

Increase Available Stock

↓

Create Inventory Ledger

↓

Purchase Completed

Automatic Actions

✔ Inventory Updated

✔ Ledger Updated

✔ Dashboard Updated

✔ Reports Updated

---

# Workflow 3 : Barcode Billing

Cashier

↓

Scan Barcode

↓

Barcode Number Received

↓

Search Medicine

↓

Medicine Found

↓

Check Available Stock

↓

Stock Available?

↓

YES

↓

Add Item To Bill

↓

Repeat Until Billing Complete

↓

Generate Sale

↓

Reduce Inventory

↓

Create Ledger Entry

↓

Dashboard Updated

↓

Reports Updated

↓

Invoice Ready

If Barcode Not Found

↓

Show

"Medicine Not Found"

---

# Workflow 4 : Manual Medicine Search

Customer requests medicine.

↓

Cashier types

Medicine Name

OR

Generic Name

↓

System Searches

↓

Display Matching Medicines

↓

Select Medicine

↓

Check Stock

↓

Add To Bill

Barcode is optional.

---

# Workflow 5 : Manual Inventory Adjustment

Admin

↓

Select Medicine

↓

Select Batch

↓

View Current Stock

↓

Enter Correct Quantity

↓

Select Adjustment Reason

↓

Save

↓

Inventory Updated

↓

Ledger Created

↓

Dashboard Updated

Reasons

Wrong Entry

Damage

Physical Count

Supplier Correction

Expired

Other

Reason is mandatory.

---

# Workflow 6 : Physical Stock Verification

Admin

↓

Select Medicine

↓

System Stock Displayed

↓

Count Physical Stock

↓

Difference Found?

↓

Yes

↓

Create Adjustment

↓

Ledger Entry

↓

Inventory Updated

↓

Verification Completed

No Difference

↓

Verification Completed

---

# Workflow 7 : Customer Return

Customer Returns Medicine

↓

Verify Medicine

↓

Verify Batch

↓

Verify Expiry

↓

Accept Return?

↓

Yes

↓

Increase Inventory

↓

Create Ledger

↓

Reports Updated

If Rejected

↓

No Inventory Change

---

# Workflow 8 : Supplier Return

Medicine Returned To Supplier

↓

Select Purchase Batch

↓

Enter Quantity

↓

Validate Quantity

↓

Reduce Inventory

↓

Ledger Entry

↓

Supplier Return Completed

---

# Workflow 9 : Expired Medicine

Daily Check

↓

Find Expired Batches

↓

Move Available Qty

↓

Expired Qty

↓

Create Ledger

↓

Dashboard Updated

↓

Report Updated

Expired medicines cannot be sold.

---

# Workflow 10 : Dashboard

Dashboard should never calculate data manually.

Dashboard reads data from

Inventory

Sales

Purchases

Ledger

Reports

Everything is generated automatically.

---

# Workflow 11 : Reports

Reports are generated from database.

Reports include

Purchase Report

Sales Report

Inventory Report

Stock Movement Report

Low Stock Report

Expiry Report

Reports should always use real database records.

Never calculate values on frontend.

---

# Global Business Rules

Rule 1

Medicine creation does not increase stock.

---

Rule 2

Purchase always increases stock.

---

Rule 3

Sale always decreases stock.

---

Rule 4

Returns always create ledger entries.

---

Rule 5

Adjustments always require reasons.

---

Rule 6

Negative stock is never allowed.

---

Rule 7

Expired medicines cannot be sold.

---

Rule 8

Every stock movement creates a ledger entry.

---

Rule 9

Inventory can only change through Inventory Service.

---

Rule 10

Medicine Master never stores stock.

---

# Module Responsibility Matrix

Medicine Module

✔ Medicine Information

✘ Stock

---------------------------------

Purchase Module

✔ Purchase Entry

✘ Manual Stock Update

---------------------------------

Inventory Module

✔ Stock

✔ Batch

✔ Ledger

---------------------------------

Sales Module

✔ Billing

✔ Sale

✘ Direct Stock Update

---------------------------------

Dashboard Module

✔ Analytics

✘ Business Logic

---------------------------------

Reports Module

✔ Read Data

✘ Modify Data

---

# Success Workflow

Login

↓

Create Medicine

↓

Purchase

↓

Inventory Updated

↓

Barcode Scan

↓

Billing

↓

Sale

↓

Inventory Reduced

↓

Ledger Updated

↓

Dashboard Updated

↓

Reports Updated

If this complete workflow works correctly, the POC is considered functionally complete.

---

# End of Document