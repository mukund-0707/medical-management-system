# Inventory Architecture

Version : 2.0

Project : Medical Store Management System (MSMS)

Priority : Critical

---

# 1. Purpose

Inventory is the most important component of the Medical Store Management System.

Every business operation ultimately affects inventory.

This document defines how inventory behaves throughout the entire application.

Every future module must follow these rules.

No module is allowed to modify inventory outside this architecture.

---

# 2. Inventory Philosophy

Inventory is NOT just a number.

Inventory is a business state.

The available stock of a medicine is always the result of business operations.

Example

Purchase

+100

↓

Sale

-5

↓

Damage

-2

↓

Customer Return

+1

↓

Final Available Stock

94

Inventory should never be edited directly.

---

# 3. Inventory Ownership

Only the Inventory Module owns inventory.

No other module has permission to update stock directly.

Responsibilities

Inventory Module

✔ Increase Stock

✔ Reduce Stock

✔ Manual Adjustment

✔ Physical Verification

✔ Batch Tracking

✔ Stock Ledger

✔ Expiry Tracking

Other modules must request inventory updates through Inventory Services.

---

# 4. Inventory Events

Inventory changes only when one of the following events occurs.

Purchase

↓

Increase Stock

Sale

↓

Decrease Stock

Customer Return

↓

Increase Stock

Supplier Return

↓

Decrease Stock

Manual Adjustment

↓

Increase or Decrease

Expired Medicine

↓

Move to Expired Stock

Damaged Medicine

↓

Move to Damaged Stock

Physical Verification

↓

Adjustment Entry

No other operation should affect inventory.

---

# 5. Inventory States

A medicine does not have only one stock value.

Inventory is divided into logical states.

Available Stock

Medicines ready for sale.

Reserved Stock

Medicines reserved for an invoice.

Damaged Stock

Medicines that cannot be sold.

Expired Stock

Expired medicines.

Returned Stock

Returned medicines waiting for verification.

Future states may be added without changing existing architecture.

---

# 6. Inventory Flow

Purchase

↓

Available Stock

↓

Sale

↓

Available Stock Reduced

↓

Customer Return

↓

Available Stock Increased

↓

Expiry

↓

Expired Stock

↓

Damage

↓

Damaged Stock

Inventory continuously changes through business events.

---

# 7. Automatic Inventory

The system automatically updates inventory after successful operations.

Purchase Saved

↓

Increase Inventory

Sale Completed

↓

Reduce Inventory

Customer Return

↓

Increase Inventory

Supplier Return

↓

Reduce Inventory

Manual calculation should never be required.

---

# 8. Manual Inventory Adjustment

Although inventory is automatic, manual correction is necessary in real-world scenarios.

Examples

- Wrong Purchase Entry
- Wrong Sale Entry
- Damaged Medicines
- Lost Medicines
- Physical Count Difference
- Supplier Correction

Inventory Adjustment allows controlled correction.

---

# 9. Inventory Adjustment Rules

Every adjustment must contain

Medicine

Batch

Previous Quantity

New Quantity

Difference

Reason

Remarks

Adjusted By

Adjustment Date

Without a reason, adjustment is not allowed.

---

# 10. Physical Stock Verification

Physical verification compares

System Stock

vs

Actual Shelf Stock

Example

System

100

Shelf

98

Difference

-2

The owner can approve adjustment.

The adjustment automatically creates inventory history.

---

# 11. Stock Ledger

Every inventory movement creates a ledger entry.

Examples

Purchase

Sale

Damage

Expiry

Return

Adjustment

Ledger records are permanent.

Ledger records must never be deleted.

---

# 12. Ledger Philosophy

The Stock Ledger is the complete history of inventory.

The current stock is only the latest state.

The ledger is the truth behind every stock movement.

Example

+100 Purchase

-5 Sale

-2 Damage

+3 Adjustment

-1 Sale

Every movement remains visible forever.

---

# 13. Batch Wise Inventory

Every medicine is stored batch-wise.

Example

Medicine

Dolo 650

Batch A

100 Qty

Expiry

2027

Batch B

50 Qty

Expiry

2028

Inventory is maintained separately for every batch.

---

# 14. Batch Rules

Different batches must never be merged.

Each batch maintains

Batch Number

Purchase Price

MRP

Expiry

Quantity

Status

Every sale reduces stock from a specific batch.

---

# 15. Sale Priority

When multiple batches exist,

the oldest valid batch should be sold first.

Priority

Nearest Expiry

↓

Next Expiry

↓

Latest Expiry

This minimizes expiry loss.

---

# 16. Expired Medicines

Expired medicines should never remain inside available stock.

Instead

Available

↓

Expired

Expired medicines remain visible for reports.

They cannot be sold.

---

# 17. Damaged Medicines

Damaged medicines should never disappear.

Instead

Available

↓

Damaged

This keeps inventory accurate.

---

# 18. Stock Validation

Before every sale

Inventory checks

Available Quantity

↓

Enough?

↓

Yes

↓

Sale Allowed

Else

↓

Out Of Stock

---

# 19. Negative Stock

Negative inventory is strictly prohibited.

Example

Available

5

Sale

10

Result

Rejected

The system must never allow stock below zero.

---

# 20. Inventory Rules

Rule 1

Inventory never changes directly.

---

Rule 2

Every change creates a ledger entry.

---

Rule 3

Every adjustment requires a reason.

---

Rule 4

Every sale validates stock first.

---

Rule 5

Expired medicines cannot be sold.

---

Rule 6

Damaged medicines cannot be sold.

---

Rule 7

Every batch maintains its own quantity.

---

Rule 8

Inventory history is permanent.

---

Rule 9

Inventory should always be recoverable from history.

---

# 21. Inventory Lifecycle

Purchase

↓

Available Stock

↓

Sale

↓

Reduced

↓

Return

↓

Increase

↓

Damage

↓

Damaged

↓

Expiry

↓

Expired

↓

History

Every inventory movement follows this lifecycle.

---

# 22. Future Enhancements

Future versions may support

Reserved Stock

Warehouse Transfer

Multiple Stores

Automatic Purchase Suggestions

AI Demand Prediction

Barcode Printer

RFID

These features should integrate without redesigning the inventory architecture.

---

# 23. Summary

Inventory is the core of the Medical Store Management System.

Every business module interacts with inventory through controlled business operations.

Inventory must always remain accurate, traceable, auditable, and recoverable.

This architecture ensures that stock remains reliable regardless of future system growth.

---

# End of Document