# Purchase Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

The Purchase Module is responsible for recording medicines purchased from suppliers.

A successful purchase is the only way to introduce new inventory into the system.

Purchase does not only create records.

Purchase also creates inventory batches and stock ledger entries.

---

# 2. Responsibilities

Purchase Module is responsible for

✔ Create Purchase

✔ Update Purchase (Before Finalization)

✔ Cancel Purchase

✔ Purchase History

✔ Supplier Validation

✔ Batch Creation

✔ Inventory Creation

✔ Ledger Creation

Purchase Module is NOT responsible for

✘ Billing

✘ Sales

✘ Dashboard

✘ Reports

Those modules only consume purchase data.

---

# 3. Purchase Lifecycle

Purchase Created

↓

Draft

↓

Items Added

↓

Validated

↓

Finalized

↓

Inventory Updated

↓

Completed

Once finalized,

Purchase becomes read-only.

---

# 4. Purchase Workflow

Admin

↓

Select Supplier

↓

Create Purchase

↓

Add Medicines

↓

Validate Items

↓

Save Draft

↓

Review

↓

Finalize Purchase

↓

Create Inventory Batch

↓

Increase Inventory

↓

Create Ledger

↓

Purchase Completed

---

# 5. Purchase Status

DRAFT

Purchase is editable.

Inventory is NOT updated.

FINALIZED

Inventory updated.

Purchase becomes locked.

CANCELLED

Purchase cancelled.

Inventory reversed only if no sale exists from affected batches.

---

# 6. Draft Philosophy

Draft purchases exist only for incomplete work.

Draft Purchase

↓

No Inventory

↓

No Ledger

↓

No Dashboard Update

↓

No Reports

Only finalized purchases affect business.

---

# 7. Purchase Header

Purchase contains

Supplier

Invoice Number

Invoice Date

Remarks

Status

Created By

Created At

Updated At

Purchase Header never stores medicine details.

---

# 8. Purchase Item

Each Purchase Item contains

Medicine

Batch Number

Expiry Date

Purchase Price

MRP

Quantity

GST

Discount

Every Purchase Item creates one Inventory Batch.

---

# 9. Purchase Validation

Before finalization

Validate

Supplier Active

Medicine Exists

Barcode Valid

Batch Number

Expiry Date

Purchase Price

MRP

Quantity

Duplicate Batch (same supplier + invoice + batch)

If any validation fails

Purchase cannot be finalized.

---

# 10. Batch Creation

Every Purchase Item creates exactly one Inventory Batch.

Example

Purchase

↓

Dolo

↓

Batch A

↓

100 Qty

Inventory now contains

Batch A

100 Qty

---

# 11. Inventory Update

Inventory updates only after

Purchase Finalization.

Draft purchase

↓

No Stock

Finalized purchase

↓

Stock Increased

---

# 12. Stock Ledger

Every purchase item creates one ledger entry.

Movement Type

PURCHASE

Quantity

+100

Reason

Purchase Invoice

Ledger is immutable.

---

# 13. Duplicate Invoice Rules

Same Supplier

+

Same Invoice Number

↓

Not Allowed

Different Supplier

+

Same Invoice Number

↓

Allowed

Invoice uniqueness is supplier-specific.

---

# 14. Purchase Editing

Allowed

Only while status = DRAFT

Not Allowed

After FINALIZED

Reason

Inventory already updated.

Editing finalized purchase may corrupt stock.

---

# 15. Purchase Cancellation

Draft

↓

Can Cancel Anytime

Finalized

↓

Allowed only if

No inventory has been consumed.

If stock from that batch has already been sold,

Cancellation must be rejected.

---

# 16. Purchase APIs

GET

/api/v1/purchases/

GET

/api/v1/purchases/{id}/

POST

/api/v1/purchases/

PUT

/api/v1/purchases/{id}/

PATCH

/api/v1/purchases/{id}/

POST

/api/v1/purchases/{id}/finalize/

POST

/api/v1/purchases/{id}/cancel/

GET

/api/v1/purchases/search/

---

# 17. Business Rules

Purchase does not directly update Medicine.

Purchase creates Inventory Batch.

Inventory Service updates stock.

Ledger Service records history.

Purchase Service orchestrates the workflow.

---

# 18. Transactions

Purchase Finalization must run inside one database transaction.

Steps

Save Purchase

↓

Save Purchase Items

↓

Create Inventory Batch

↓

Increase Stock

↓

Create Ledger

↓

Commit

If any step fails

↓

Rollback Everything

Partial updates are never allowed.

---

# 19. Edge Cases

Case 1

Supplier inactive

↓

Reject Purchase

---

Case 2

Medicine inactive

↓

Reject Purchase

---

Case 3

Duplicate invoice

↓

Reject

---

Case 4

Invalid expiry

↓

Reject

---

Case 5

Quantity <= 0

↓

Reject

---

Case 6

Purchase cancelled after stock sold

↓

Reject

---

Case 7

Duplicate batch number in same invoice

↓

Reject

---

# 20. Audit Logs

Log

Purchase Created

Purchase Updated

Purchase Finalized

Purchase Cancelled

Purchase Validation Failed

Duplicate Invoice Attempt

Inventory Created

Every important action should be traceable.

---

# 21. Future Enhancements

Purchase Orders

Invoice PDF Upload

OCR Invoice Reading

Supplier Credit

Payment Tracking

Purchase Approval Workflow

Bulk Import

Excel Import

---

# 22. Architect Decisions

Accepted

✔ Draft Workflow

✔ Finalization Step

✔ Batch Creation

✔ Inventory Creation

✔ Ledger Creation

✔ Transaction-Based Save

✔ Supplier Validation

✔ Duplicate Invoice Validation

Rejected

✘ Inventory Update During Draft

✘ Editing Finalized Purchase

✘ Direct Stock Update

✘ Purchase Without Supplier

---

# 23. Module Summary

Purchase Module is the entry point of inventory.

Every finalized purchase creates inventory, stock history and batch records.

A purchase is considered successful only when inventory and ledger are updated successfully inside a single transaction.

---

# End of Document