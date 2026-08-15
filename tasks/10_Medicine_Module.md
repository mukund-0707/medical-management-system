# Medicine Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

Medicine Module is responsible for maintaining the master information of medicines.

This module is the central catalog of the application.

Every business module depends on Medicine Module.

Inventory

Purchase

Sales

Barcode

Dashboard

Reports

All these modules require medicine information.

Medicine Module is NOT responsible for inventory.

---

# 2. Responsibilities

Medicine Module is responsible for

✔ Creating Medicine

✔ Updating Medicine

✔ Deactivating Medicine

✔ Searching Medicines

✔ Barcode Lookup

✔ Generic Search

✔ Listing Medicines

Medicine Module is NOT responsible for

✘ Stock

✘ Batch

✘ Expiry

✘ Purchase Price

✘ Selling Price

✘ Inventory Adjustment

Those belong to Inventory Module.

---

# 3. Medicine Lifecycle

Create Medicine

↓

Active

↓

Used In Purchase

↓

Used In Sales

↓

Inactive

Medicine should never be permanently deleted.

---

# 4. Business Philosophy

Medicine represents only product identity.

Everything that changes over time belongs somewhere else.

Medicine stores

✔ Identity

Inventory stores

✔ Quantity

Purchase stores

✔ Buying Information

Sales stores

✔ Selling Information

Keeping responsibilities separate prevents data inconsistency.

---

# 5. Medicine Creation Workflow

Admin

↓

Open Medicine Screen

↓

Enter Details

↓

Validate

↓

Check Duplicate Barcode

↓

Check Duplicate Medicine

↓

Save

↓

Medicine Created

↓

Ready For Purchase

Stock remains ZERO.

---

# 6. Mandatory Fields

Medicine Name

Barcode

Manufacturer

Dosage Form

Strength

Status

Everything else is optional.

---

# 7. Optional Fields

Generic Name

Description

Category

Storage Instruction

Medicine Image

HSN Code

GST Percentage

These fields improve search and reporting.

---

# 8. Medicine Status

ACTIVE

Medicine can be purchased and sold.

INACTIVE

Medicine is hidden from billing.

Existing history remains.

DISCONTINUED

Medicine will never be purchased again.

Historical data remains available.

---

# 9. Barcode Rules

Every medicine must have one barcode.

Barcode must be unique.

Barcode cannot be edited once medicine has purchase history.

Changing barcode after transactions may break history.

---

# 10. Duplicate Medicine Rules

Before creating a medicine

Check

Barcode

↓

Already Exists?

↓

Reject

Also compare

Medicine Name

Strength

Manufacturer

If all match

Warn user about possible duplicate.

Admin decides whether to continue.

---

# 11. Medicine Search

Search should support

Medicine Name

Generic Name

Barcode

Manufacturer

Category

Search must be case-insensitive.

Partial matching should be supported.

Example

"dol"

↓

Dolo 650

Dolo 500

---

# 12. Barcode Search

Input

8901234567890

↓

Find Medicine

↓

Return Medicine Details

If barcode does not exist

Return

Medicine Not Found

Barcode search should always use database index.

---

# 13. Editing Medicine

Allowed

Description

Category

Storage Instruction

Image

Status

Restricted

Barcode (after transactions)

Medicine Name (after transactions)

Strength (after transactions)

Manufacturer (after transactions)

Identity fields should not change after business transactions.

---

# 14. Delete Policy

Medicine should never be permanently deleted.

Instead

Status

↓

INACTIVE

Reason

Purchase

Sales

Reports

Inventory History

must remain valid forever.

---

# 15. Validation Rules

Medicine Name

Cannot be empty.

Barcode

Required

Unique

Manufacturer

Required.

Strength

Required.

Status

Required.

Leading and trailing spaces should be removed before saving.

---

# 16. Business Rules

Medicine does not own stock.

Medicine does not own batch.

Medicine does not own expiry.

Medicine does not own price.

Medicine only defines identity.

---

# 17. API Endpoints

GET

/api/v1/medicines/

GET

/api/v1/medicines/{id}/

POST

/api/v1/medicines/

PUT

/api/v1/medicines/{id}/

PATCH

/api/v1/medicines/{id}/

DELETE

/api/v1/medicines/{id}/

GET

/api/v1/medicines/search/

GET

/api/v1/medicines/barcode/{barcode}/

---

# 18. Response Example

Success

{
    "success": true,
    "message": "Medicine created successfully.",
    "data": {}
}

Failure

{
    "success": false,
    "message": "Barcode already exists.",
    "errors": {}
}

---

# 19. Performance Rules

Indexes

Barcode

Medicine Name

Generic Name

Search queries should never scan the entire table.

Always use indexed lookups where possible.

---

# 20. Audit Rules

Log

Medicine Created

Medicine Updated

Medicine Deactivated

Barcode Search Failure

Duplicate Medicine Attempt

These logs help troubleshooting.

---

# 21. Edge Cases

Case 1

Medicine already exists.

Reject duplicate barcode.

---

Case 2

Medicine is inactive.

Cannot be used for new purchase or sale.

---

Case 3

Medicine has transaction history.

Identity fields become read-only.

---

Case 4

Medicine has no transactions.

Editing is fully allowed.

---

Case 5

Barcode scanner sends unknown barcode.

System returns

Medicine Not Found.

No inventory changes occur.

---

# 22. Future Enhancements

Medicine Images

Medicine Composition

Alternative Medicines

Therapeutic Category

Manufacturer Table

Category Table

Prescription Requirement

Temperature Sensitive Flag

Schedule H / X Classification

These can be added without changing existing APIs.

---

# 23. Architect Decisions

Accepted

✔ Medicine stores identity only.

✔ Barcode is unique.

✔ Soft Delete only.

✔ Barcode lookup is indexed.

✔ Identity becomes immutable after transactions.

Rejected

✘ Stock inside Medicine.

✘ MRP inside Medicine.

✘ Batch inside Medicine.

✘ Expiry inside Medicine.

✘ Direct deletion.

---

# 24. Module Summary

Medicine Module is the master catalog of the application.

Its only responsibility is to identify medicines.

Inventory, pricing, stock and business transactions are managed by their respective modules.

Keeping the Medicine Module clean ensures that every other module remains simple, predictable and scalable.

---

# End of Document