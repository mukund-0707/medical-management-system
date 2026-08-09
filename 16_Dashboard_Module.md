# Dashboard Module

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : High

---

# 1. Purpose

The Dashboard Module provides a quick overview of the current business status.

Its primary goal is to help the owner understand the health of the medical store without opening multiple screens.

The Dashboard is a read-only module.

It never modifies business data.

---

# 2. Responsibilities

Dashboard Module is responsible for

✔ Business Summary

✔ Inventory Summary

✔ Sales Summary

✔ Purchase Summary

✔ Low Stock Alerts

✔ Expiry Alerts

✔ Quick Statistics

✔ Recent Activities

Dashboard Module is NOT responsible for

✘ Inventory Update

✘ Purchase

✘ Sales

✘ Reports

---

# 3. Dashboard Philosophy

Dashboard never owns data.

Dashboard only reads data from

Inventory

Sales

Purchase

Inventory Ledger

Medicine

No calculations should update business records.

---

# 4. Dashboard Layout

The dashboard contains

Top KPI Cards

↓

Alert Section

↓

Charts

↓

Recent Activities

↓

Quick Actions

The layout should remain simple and responsive.

---

# 5. KPI Cards

Display

Today's Sales

Today's Purchases

Current Inventory Value

Available Medicines

Low Stock Count

Expired Batch Count

These values should load quickly.

---

# 6. Inventory Summary

Display

Total Medicines

Total Inventory Quantity

Low Stock Medicines

Out Of Stock Medicines

Expired Batches

Damaged Stock

Inventory summary should use Inventory Batch.

Never calculate using Ledger.

---

# 7. Sales Summary

Display

Today's Sales

Today's Invoice Count

Average Invoice Value

Top Selling Medicines

Recent Sales

Sales data should be filtered by selected date.

---

# 8. Purchase Summary

Display

Today's Purchases

Purchase Count

Recent Purchases

Latest Supplier

Purchase summaries are read-only.

---

# 9. Alerts

Dashboard should display

Low Stock

Expired Medicines

Near Expiry Medicines

Inactive Medicines

Alerts should be sorted by priority.

Critical alerts appear first.

---

# 10. Recent Activities

Display latest activities

Medicine Added

Purchase Finalized

Inventory Adjusted

Sale Completed

Purchase Cancelled

Customer Return

Supplier Return

Activities should display

Date

Time

User

Action

Reference Number

---

# 11. Quick Actions

Dashboard should provide shortcuts

Add Medicine

New Purchase

Start Billing

Inventory Adjustment

View Reports

These are navigation shortcuts only.

---

# 12. Charts

POC Charts

Daily Sales

Purchase Trend

Top Selling Medicines

Inventory Distribution

Future charts

Monthly Sales

Profit Trend

Category Analysis

Supplier Analysis

---

# 13. Dashboard Filters

Supported filters

Today

Yesterday

This Week

This Month

Custom Date Range

Every widget should respect selected filters.

---

# 14. Performance

Dashboard should load within

2 Seconds

Maximum.

Avoid expensive queries.

Use aggregation.

Avoid N+1 queries.

Indexes should be used wherever possible.

---

# 15. API Endpoints

GET

/api/v1/dashboard/

GET

/api/v1/dashboard/sales/

GET

/api/v1/dashboard/purchases/

GET

/api/v1/dashboard/inventory/

GET

/api/v1/dashboard/alerts/

GET

/api/v1/dashboard/activities/

---

# 16. Business Rules

Dashboard is read-only.

Dashboard never updates inventory.

Dashboard never creates business records.

Dashboard should remain independent.

---

# 17. Edge Cases

Case 1

No sales today.

↓

Display

0

Do not show errors.

---

Case 2

No purchases today.

↓

Display

0

---

Case 3

No low stock.

↓

Hide alert section.

---

Case 4

No expired medicines.

↓

Display

"No expired medicines."

---

Case 5

Large inventory.

↓

Dashboard should still remain responsive.

---

# 18. Audit

Dashboard itself does not create audit records.

Audit information is read from business modules.

---

# 19. Future Enhancements

Profit Dashboard

AI Insights

Sales Forecast

Demand Prediction

Supplier Analytics

Customer Analytics

Store Comparison

Multi Branch Dashboard

Notification Center

---

# 20. Architect Decisions

Accepted

✔ Read-Only Dashboard

✔ KPI Cards

✔ Alert Driven Design

✔ Aggregated Queries

✔ Fast Loading

Rejected

✘ Business Logic

✘ Inventory Updates

✘ Direct Calculations from Ledger

---

# 21. Module Summary

The Dashboard Module provides business visibility without modifying data.

It acts as the central monitoring screen for the medical store owner and presents real-time operational information through optimized read-only queries.

---

# End of Document