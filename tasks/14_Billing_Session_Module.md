# Billing Session Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

The Billing Session Module represents the temporary bill that is prepared before a sale is completed.

A billing session allows the cashier to scan medicines, modify quantities, remove items, apply discounts and review the bill before checkout.

A Billing Session is temporary.

It does not affect inventory until checkout is completed.

---

# 2. Responsibilities

Billing Session is responsible for

✔ Create Cart

✔ Add Item

✔ Remove Item

✔ Change Quantity

✔ Hold Current Bill (Future)

✔ Calculate Totals

✔ Validate Availability

✔ Checkout Request

Billing Session is NOT responsible for

✘ Inventory Update

✘ Ledger Entry

✘ Sale Creation

✘ Dashboard

---

# 3. Billing Session Lifecycle

Create Session

↓

Add Items

↓

Modify Items

↓

Validate Stock

↓

Checkout

↓

Generate Sale

↓

Destroy Session

If cancelled

↓

Destroy Session

No inventory changes occur.

---

# 4. Billing Workflow

Cashier

↓

Open Billing Screen

↓

New Session Created

↓

Scan Medicine

↓

Medicine Added

↓

Modify Quantity

↓

Repeat Until Complete

↓

Checkout

↓

Sales Module

↓

Inventory Module

↓

Ledger

↓

Invoice

↓

Session Closed

---

# 5. Session Rules

One active session per billing screen.

Every session has a unique identifier.

A session expires automatically after inactivity.

Expired sessions never affect inventory.

---

# 6. Add Item Workflow

Scan Barcode

↓

Medicine Found

↓

Medicine Active

↓

Stock Available

↓

Add Item

↓

Recalculate Bill

If medicine already exists in cart

↓

Increase Quantity

Do not create duplicate rows.

---

# 7. Remove Item Workflow

Select Item

↓

Remove

↓

Recalculate Total

↓

Session Updated

Inventory remains unchanged.

---

# 8. Update Quantity Workflow

Select Item

↓

Enter New Quantity

↓

Validate Stock

↓

Update Quantity

↓

Recalculate Total

If requested quantity exceeds available stock

↓

Reject update.

---

# 9. Cart Calculation

Every modification recalculates

Subtotal

Discount

GST

Grand Total

Round Off (if configured)

The frontend should display values returned by the backend.

Business calculations remain in the backend.

---

# 10. Checkout Workflow

Cashier

↓

Click Checkout

↓

Validate Session

↓

Validate Stock Again

↓

Generate Sale

↓

Update Inventory

↓

Create Ledger

↓

Generate Invoice

↓

Close Session

↓

Return Success

---

# 11. Session Validation

Before checkout

Validate

Session Exists

Session Active

Items Exist

Medicine Active

Stock Available

No validation should rely on earlier checks only.

Everything must be validated again.

---

# 12. Stock Revalidation

Stock is validated

While adding item

AND

Again before checkout.

Reason

Another billing counter may have sold the same medicine.

Final validation always happens before sale creation.

---

# 13. Session Expiry

Inactive Session

↓

Configured Timeout

↓

Auto Expire

↓

Session Deleted

Inventory remains unchanged.

---

# 14. Cancel Session

Cashier

↓

Cancel

↓

Delete Session

↓

Return Success

No ledger.

No inventory.

No sale.

---

# 15. API Endpoints

POST

/api/v1/billing/session/

GET

/api/v1/billing/session/{id}/

POST

/api/v1/billing/session/{id}/items/

PATCH

/api/v1/billing/session/{id}/items/{item_id}/

DELETE

/api/v1/billing/session/{id}/items/{item_id}/

POST

/api/v1/billing/session/{id}/checkout/

DELETE

/api/v1/billing/session/{id}/

---

# 16. Business Rules

Billing Session is temporary.

Billing Session never owns inventory.

Billing Session never updates stock.

Checkout is the only operation that creates a sale.

---

# 17. Edge Cases

Case 1

Medicine becomes inactive during billing.

↓

Reject checkout.

---

Case 2

Stock reduced by another sale.

↓

Reject checkout.

Ask cashier to refresh.

---

Case 3

Empty cart.

↓

Checkout not allowed.

---

Case 4

Duplicate scan.

↓

Increase quantity.

Do not create duplicate rows.

---

Case 5

Session expired.

↓

Reject checkout.

Create new session.

---

# 18. Audit Logs

Session Created

Item Added

Item Removed

Quantity Changed

Checkout Completed

Checkout Failed

Session Cancelled

Session Expired

---

# 19. Future Enhancements

Hold Bill

Resume Bill

Multiple Billing Counters

Customer Attachment

Prescription Attachment

Loyalty Points

Coupon Engine

Gift Voucher

Split Payment

---

# 20. Architect Decisions

Accepted

✔ Temporary Session

✔ Inventory Independent

✔ Double Stock Validation

✔ Auto Session Expiry

✔ Backend Calculations

Rejected

✘ Inventory Update During Scan

✘ Permanent Cart Storage

✘ Frontend Price Calculation

---

# 21. Module Summary

The Billing Session Module acts as the bridge between barcode scanning and final sales.

It provides a safe environment where medicines can be added, modified and validated before any inventory movement occurs.

Only after a successful checkout does the Sales Module create the sale and trigger inventory updates.

---

# End of Document