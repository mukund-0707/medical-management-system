# Report Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : High

---

# 1. Purpose

The Report Module provides historical, operational and analytical information about the medical store.

Reports help the owner understand business performance, inventory movement and purchasing trends.

Reports are completely read-only.

No report should modify business data.

---

# 2. Responsibilities

The Report Module is responsible for

✔ Sales Reports

✔ Purchase Reports

✔ Inventory Reports

✔ Stock Movement Reports

✔ Expiry Reports

✔ Low Stock Reports

✔ Inventory Adjustment Reports

✔ Audit Reports

The Report Module is NOT responsible for

✘ Purchase

✘ Sales

✘ Inventory Update

✘ Dashboard

---

# 3. Report Philosophy

Reports never own data.

Reports only read data from

Purchase

Purchase Item

Sale

Sale Item

Inventory Batch

Inventory Ledger

Medicine

Supplier

---

# 4. Available Reports

The POC includes

Sales Report

Purchase Report

Inventory Report

Stock Ledger Report

Low Stock Report

Expiry Report

Adjustment Report

Medicine Report

Supplier Report

---

# 5. Sales Report

Display

Invoice Number

Invoice Date

Total Amount

Payment Mode

Discount

GST

Created By

Support Filters

Date

Invoice Number

Payment Mode

Medicine

---

# 6. Purchase Report

Display

Supplier

Invoice Number

Purchase Date

Purchase Total

Total Items

Created By

Support Filters

Supplier

Date

Invoice Number

Medicine

---

# 7. Inventory Report

Display

Medicine

Batch

Expiry

Available Quantity

Damaged Quantity

Expired Quantity

Purchase Price

MRP

Support Filters

Medicine

Batch

Category

Status

---

# 8. Stock Movement Report

Read data from Inventory Ledger.

Display

Movement Type

Reference

Medicine

Batch

Quantity

Reason

Created By

Created At

This report becomes the audit history of stock.

---

# 9. Low Stock Report

Display all medicines where

Available Quantity

<=

Configured Low Stock Level

Sort

Lowest Quantity First

---

# 10. Expiry Report

Display

Expired Medicines

Near Expiry Medicines

Batch Number

Expiry Date

Remaining Quantity

Support Filters

30 Days

60 Days

90 Days

Custom Range

---

# 11. Adjustment Report

Display

Medicine

Batch

Previous Quantity

New Quantity

Difference

Reason

Adjusted By

Adjusted Date

---

# 12. Medicine Report

Display

Medicine

Manufacturer

Category

Status

Barcode

Number of Batches

Current Available Quantity

---

# 13. Supplier Report

Display

Supplier Name

Purchase Count

Latest Purchase Date

Status

Total Purchase Value (Future)

---

# 14. Filters

All reports support

Date Range

Medicine

Supplier

Batch

Invoice Number

Status

Search

Reports should never require manual filtering.

---

# 15. Export

POC

Screen View

Future

Excel

CSV

PDF

Print

Email

---

# 16. Performance

Reports must use pagination.

Heavy reports should never load all records.

Use indexed queries.

Aggregation should happen in database whenever possible.

---

# 17. API Endpoints

GET

/api/v1/reports/sales/

GET

/api/v1/reports/purchases/

GET

/api/v1/reports/inventory/

GET

/api/v1/reports/ledger/

GET

/api/v1/reports/expiry/

GET

/api/v1/reports/low-stock/

GET

/api/v1/reports/adjustments/

GET

/api/v1/reports/medicines/

GET

/api/v1/reports/suppliers/

---

# 18. Business Rules

Reports are read-only.

Reports never update data.

Reports should always show historical records.

Deleted or inactive records must remain visible if they belong to historical transactions.

---

# 19. Edge Cases

Case 1

No records found.

↓

Return empty list.

Do not return errors.

---

Case 2

Large date range.

↓

Use pagination.

---

Case 3

Inactive medicine.

↓

Still display historical records.

---

Case 4

Cancelled purchase.

↓

Display with status.

Do not hide.

---

Case 5

Cancelled sale.

↓

Display with status.

Do not remove from reports.

---

# 20. Audit

Reports should accurately reflect the underlying business records.

Reports themselves do not create audit entries.

Audit data is read from Inventory Ledger and business transaction tables.

---

# 21. Future Enhancements

Profit & Loss Report

GST Report

Daily Closing Report

Monthly Closing Report

Fast Moving Medicines

Slow Moving Medicines

ABC Analysis

XYZ Analysis

Dead Stock Report

Supplier Performance Report

Customer Purchase Report

Inventory Valuation Report

AI Business Insights

---

# 22. Architect Decisions

Accepted

✔ Read-Only Reports

✔ Database-Level Filtering

✔ Pagination

✔ Historical Data Preservation

✔ Ledger-Based Stock Movement Report

Rejected

✘ Business Logic Inside Reports

✘ Data Modification

✘ Manual Calculations on Frontend

---

# 23. Module Summary

The Report Module provides complete business visibility through structured, filterable and historical reports.

It enables informed decision making while preserving the integrity of business data.

Reports remain independent from operational modules and only consume validated data.

---

# End of Document