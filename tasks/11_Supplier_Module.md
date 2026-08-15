# Supplier Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : High

---

# 1. Purpose

Supplier Module is responsible for managing all medicine suppliers.

Every purchase must be linked to a supplier.

The Supplier Module acts as the master database of vendors supplying medicines to the medical store.

The module is responsible only for supplier information.

It does not manage purchases or inventory.

---

# 2. Responsibilities

Supplier Module is responsible for

✔ Supplier Registration

✔ Supplier Information

✔ Supplier Search

✔ Supplier Update

✔ Supplier Status

✔ Supplier Listing

Supplier Module is NOT responsible for

✘ Purchase

✘ Inventory

✘ Payment

✘ Medicine Stock

---

# 3. Supplier Lifecycle

Create Supplier

↓

Active

↓

Used In Purchase

↓

Inactive

Supplier should never be permanently deleted.

---

# 4. Business Workflow

Admin

↓

Add Supplier

↓

Validate Details

↓

Save Supplier

↓

Supplier Ready

↓

Purchase Can Be Created

---

# 5. Mandatory Fields

Supplier Name

Mobile Number

Address

Status

---

# 6. Optional Fields

GST Number

Drug License Number

Email

Contact Person

City

State

Country

Pincode

Remarks

---

# 7. Supplier Status

ACTIVE

Supplier available for purchase.

INACTIVE

Cannot create new purchases.

Purchase history remains.

BLACKLISTED (Future)

Supplier temporarily blocked.

---

# 8. Validation Rules

Supplier Name

Cannot be empty.

Phone Number

Must be valid.

GST Number

Optional

Must follow valid format if provided.

Email

Optional

Must be valid.

Duplicate supplier names should generate warning.

---

# 9. Duplicate Detection

Before creating supplier

Compare

Supplier Name

Phone Number

GST Number

If exact match exists

Warn Admin

Possible Duplicate Supplier

Admin decides whether to continue.

---

# 10. Search

Search should support

Supplier Name

Phone Number

GST Number

Contact Person

Search should be

Case Insensitive

Partial Match

Fast

---

# 11. Editing Supplier

Allowed

Phone

Address

Email

Contact Person

Remarks

Status

Restricted

Supplier Name (after purchase history)

GST Number (after purchase history)

Identity information should remain stable.

---

# 12. Delete Policy

Supplier should never be deleted.

Reason

Purchase history depends on Supplier.

Deleting supplier breaks reports.

Instead

Status

↓

INACTIVE

---

# 13. Purchase Dependency

Purchase cannot exist without Supplier.

Supplier must exist.

Supplier must be ACTIVE.

Inactive suppliers cannot receive new purchase orders.

---

# 14. Business Rules

Supplier never owns medicines.

Supplier never owns inventory.

Supplier only supplies medicines.

Inventory ownership starts after purchase completion.

---

# 15. API Endpoints

GET

/api/v1/suppliers/

GET

/api/v1/suppliers/{id}/

POST

/api/v1/suppliers/

PUT

/api/v1/suppliers/{id}/

PATCH

/api/v1/suppliers/{id}/

DELETE

/api/v1/suppliers/{id}/

GET

/api/v1/suppliers/search/

---

# 16. Standard Response

Success

{
    "success": true,
    "message": "Supplier created successfully.",
    "data": {}
}

Failure

{
    "success": false,
    "message": "Supplier already exists.",
    "errors": {}
}

---

# 17. Audit Logs

Create log when

Supplier Created

Supplier Updated

Supplier Deactivated

Duplicate Supplier Attempt

Status Changed

Logs should never be deleted.

---

# 18. Reports

Supplier module provides data for

Purchase Report

Supplier Purchase History

Supplier-wise Purchases

Supplier Performance (Future)

Outstanding Payments (Future)

---

# 19. Edge Cases

Case 1

Supplier has purchase history.

↓

Cannot Delete

Only Inactivate.

---

Case 2

Supplier inactive.

↓

New Purchase Not Allowed.

---

Case 3

Duplicate GST Number.

↓

Reject.

---

Case 4

Duplicate Phone Number.

↓

Warn User.

---

Case 5

Supplier without GST.

↓

Allowed.

---

# 20. Future Enhancements

Outstanding Payment Tracking

Supplier Rating

Purchase Analytics

Preferred Supplier

Credit Limit

Payment Terms

Purchase Orders

Email Integration

These features should integrate without changing existing APIs.

---

# 21. Architect Decisions

Accepted

✔ Soft Delete

✔ Purchase Dependency

✔ Duplicate Detection

✔ Search Support

✔ Supplier Status

Rejected

✘ Permanent Delete

✘ Inventory Ownership

✘ Purchase Logic Inside Supplier

---

# 22. Module Summary

Supplier Module is a master module.

It stores supplier identity and enables purchase operations.

Business operations like Purchase, Inventory and Payments remain independent modules.

---

# End of Document