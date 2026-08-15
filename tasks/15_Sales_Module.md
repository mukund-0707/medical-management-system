# Sales Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

The Sales Module is responsible for converting a Billing Session into a completed business transaction.

A successful sale records customer purchases, updates inventory, generates invoice details and creates stock movement history.

A sale is considered complete only when all related business operations are successfully committed.

---

# 2. Responsibilities

Sales Module is responsible for

✔ Checkout

✔ Sale Creation

✔ Sale Item Creation

✔ Payment Information

✔ Invoice Number Generation

✔ Inventory Deduction

✔ Ledger Creation

✔ Sale History

✔ Sale Cancellation Rules

Sales Module is NOT responsible for

✘ Barcode Lookup

✘ Purchase

✘ Inventory Logic

✘ Reports

✘ Dashboard

Those modules receive data from Sales Module.

---

# 3. Sales Workflow

Billing Session

↓

Validate Session

↓

Validate Stock

↓

Create Sale

↓

Create Sale Items

↓

Reduce Inventory

↓

Create Ledger Entries

↓

Generate Invoice Number

↓

Commit Transaction

↓

Return Success

---

# 4. Sales Lifecycle

Billing Session

↓

Checkout

↓

Completed Sale

↓

Invoice Generated

↓

History Available

Sale records are permanent.

---

# 5. Sale Header

The Sale table stores

Invoice Number

Sale Date

Payment Mode

Subtotal

Discount

GST

Grand Total

Round Off

Remarks

Created By

Created At

The Sale table never stores medicine details.

---

# 6. Sale Item

Each Sale Item stores

Sale

Medicine

Inventory Batch

Quantity

Selling Price

Discount

GST

Total Amount

Every Sale Item must reference the Inventory Batch used.

---

# 7. Payment Modes

Supported

Cash

UPI

Card

Bank Transfer

Mixed Payment (Future)

Payment Mode is mandatory.

Payment processing is outside the scope of this project.

The system only records payment information.

---

# 8. Invoice Number

Invoice Number must be generated automatically.

It should remain unique.

Invoice numbers must never be reused.

Even cancelled sales keep their invoice number.

---

# 9. Stock Validation

Before creating the sale

Validate

Billing Session Exists

↓

Items Exist

↓

Medicine Active

↓

Inventory Available

↓

Inventory Batch Available

↓

Proceed

Validation must occur immediately before database transaction.

---

# 10. Inventory Deduction

Sales Module never updates inventory directly.

Instead

Sales Module

↓

Inventory Service

↓

Batch Selection (FEFO)

↓

Inventory Reduced

↓

Ledger Created

---

# 11. Multi Batch Sales

One sale item may consume multiple inventory batches.

Example

Customer buys

10 Tablets

Inventory

Batch A

6 Tablets

Batch B

20 Tablets

System

Batch A

↓

6

Batch B

↓

4

Sale remains one logical item.

Inventory handles batch allocation internally.

---

# 12. Database Transaction

Checkout must execute inside one transaction.

Create Sale

↓

Create Sale Items

↓

Reduce Inventory

↓

Create Ledger

↓

Commit

If any operation fails

↓

Rollback Everything

Partial sales are never allowed.

---

# 13. Sale Cancellation

Completed sales cannot be edited.

Cancellation is allowed only through the cancellation workflow.

Cancellation must reverse inventory only if business rules allow.

Future versions may replace cancellation with Sale Return.

---

# 14. Business Rules

Sale cannot exist without Sale Items.

Sale cannot be created with empty cart.

Negative stock is prohibited.

Inactive medicines cannot be sold.

Expired medicines cannot be sold.

Damaged medicines cannot be sold.

Inventory is always reduced through Inventory Service.

---

# 15. API Endpoints

GET

/api/v1/sales/

GET

/api/v1/sales/{id}/

POST

/api/v1/sales/checkout/

GET

/api/v1/sales/invoice/{invoice_number}/

POST

/api/v1/sales/{id}/cancel/

---

# 16. Response Format

Success

{
    "success": true,
    "message": "Sale completed successfully.",
    "data": {
        "invoice_number": "INV-20260804-0001"
    }
}

Failure

{
    "success": false,
    "message": "Insufficient stock available.",
    "errors": {}
}

---

# 17. Audit Logs

Sale Created

Sale Cancelled

Checkout Failed

Inventory Deducted

Invoice Generated

Payment Recorded

Every completed sale must leave an audit trail.

---

# 18. Edge Cases

Case 1

Billing Session expired.

↓

Reject checkout.

---

Case 2

Stock changed during billing.

↓

Reject checkout.

Ask cashier to refresh.

---

Case 3

Medicine became inactive.

↓

Reject checkout.

---

Case 4

Invoice number generation failed.

↓

Rollback transaction.

---

Case 5

Inventory deduction failed.

↓

Rollback transaction.

---

Case 6

Database error during checkout.

↓

Rollback everything.

---

# 19. Future Enhancements

Customer Module

Sale Return

Exchange

Credit Sale

Partial Payment

Split Payment

Online Payment Gateway

E-Invoice

Thermal Printer

Loyalty Program

---

# 20. Architect Decisions

Accepted

✔ Transaction-Based Checkout

✔ Immutable Sale History

✔ Inventory Service Ownership

✔ Automatic Invoice Number

✔ Multi Batch Consumption

Rejected

✘ Editing Completed Sale

✘ Direct Inventory Update

✘ Manual Invoice Number

✘ Partial Transaction Save

---

# 21. Module Summary

The Sales Module represents the final business transaction of the billing process.

Its responsibility is to convert a validated Billing Session into a completed sale while ensuring inventory, ledger and invoice information remain consistent.

Every completed sale must be atomic, traceable and recoverable.

---

# End of Document