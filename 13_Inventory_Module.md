# Barcode Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

The Barcode Module provides fast and reliable identification of medicines.

The barcode scanner does not understand medicines.

It only sends a barcode number.

The backend identifies the medicine, validates inventory and returns complete medicine information.

The Barcode Module never updates inventory.

Inventory changes only after a successful sale.

---

# 2. Responsibilities

Barcode Module is responsible for

✔ Barcode Lookup

✔ Medicine Identification

✔ Barcode Validation

✔ Fast Search

✔ Unknown Barcode Detection

Barcode Module is NOT responsible for

✘ Sales

✘ Purchase

✘ Inventory

✘ Billing

✘ Reports

---

# 3. Barcode Philosophy

Barcode Scanner

↓

Reads Barcode

↓

Sends Number

↓

Backend Search

↓

Medicine Found

↓

Return Details

Scanner only works as an input device.

Business logic always remains inside backend.

---

# 4. Barcode Workflow

Customer

↓

Cashier Scans Barcode

↓

Scanner Sends Barcode Number

↓

Backend Receives Barcode

↓

Search Medicine

↓

Medicine Found?

↓

YES

↓

Return Medicine Details

↓

Frontend Adds Medicine To Cart

↓

Wait For Checkout

Inventory is NOT updated here.

---

# 5. Unknown Barcode

Barcode

↓

Search

↓

Not Found

↓

Return

"Medicine Not Found"

The system should never create medicines automatically.

Only Admin can register new medicines.

---

# 6. Barcode Search Rules

Search should be

Exact Match

Indexed

Case Independent (where applicable)

Very Fast

Target response time

< 100 milliseconds

---

# 7. Multiple Packaging (Future)

Future versions may support

Box Barcode

Strip Barcode

Bottle Barcode

Loose Unit Barcode

All barcodes will map to the same medicine.

Inventory will always remain in Base Unit.

---

# 8. Offline Scanner Support

Most USB Barcode Scanners work as keyboard devices.

Example

8901234567890

↓

Enter Key

The frontend should automatically detect Enter and perform barcode lookup.

No special scanner SDK is required.

---

# 9. Barcode Validation

Barcode cannot be empty.

Barcode length must be valid.

Unknown barcode returns Not Found.

Inactive medicine cannot be billed.

---

# 10. Barcode Search Response

Return

Medicine ID

Medicine Name

Strength

Manufacturer

Available Quantity

Package Information

Status

The Barcode Module never returns purchase information.

---

# 11. Business Rules

Barcode only identifies medicine.

Barcode never creates sale.

Barcode never updates stock.

Barcode never creates invoice.

Barcode lookup is read-only.

---

# 12. API Endpoints

GET

/api/v1/barcodes/{barcode}/

POST

/api/v1/barcodes/lookup/

Both endpoints return identical business information.

---

# 13. Performance

Barcode field must be indexed.

Barcode lookup should always use indexed queries.

Full table scans are prohibited.

---

# 14. Edge Cases

Case 1

Unknown Barcode

↓

Return Not Found.

---

Case 2

Inactive Medicine

↓

Reject Billing.

---

Case 3

Duplicate Barcode

↓

Should never happen.

Database constraint prevents this.

---

Case 4

Scanner Sends Extra Enter

↓

Ignore duplicate request.

---

Case 5

Network Delay

↓

Frontend may retry lookup.

Lookup should remain idempotent.

---

# 15. Audit Logs

Log

Unknown Barcode

Barcode Lookup Failure

Duplicate Barcode Attempt

Inactive Medicine Lookup

Successful Lookup (Optional)

---

# 16. Future Enhancements

QR Code

Data Matrix

GS1 Barcode

Package-Level Barcode

Barcode Printing

Mobile Camera Scanner

---

# 17. Architect Decisions

Accepted

✔ Indexed Barcode Lookup

✔ Read Only Module

✔ Unknown Barcode Handling

✔ Inventory Independent

Rejected

✘ Barcode Creates Sale

✘ Barcode Updates Inventory

✘ Auto Medicine Creation

---

# 18. Summary

Barcode Module is an identification module.

Its only responsibility is to convert a scanned barcode into a valid medicine record.

Business operations such as inventory updates and billing remain the responsibility of their respective modules.

---

# End of Document