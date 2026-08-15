"""
Custom business exceptions for MSMS.
These map to meaningful HTTP status codes and messages.
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class BusinessRuleException(APIException):
    """Base class for business rule violations (HTTP 422)."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'A business rule was violated.'
    default_code = 'business_rule_error'


class OutOfStockException(BusinessRuleException):
    default_detail = 'Requested quantity exceeds available stock.'
    default_code = 'out_of_stock'


class DuplicateBarcodeException(BusinessRuleException):
    default_detail = 'Barcode already exists.'
    default_code = 'duplicate_barcode'


class InvalidBatchException(BusinessRuleException):
    default_detail = 'Invalid or expired batch.'
    default_code = 'invalid_batch'


class MedicineNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Medicine not found.'
    default_code = 'medicine_not_found'


class SupplierNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Supplier not found.'
    default_code = 'supplier_not_found'


class InactiveMedicineException(BusinessRuleException):
    default_detail = 'This medicine is inactive and cannot be used.'
    default_code = 'inactive_medicine'


class ExpiredMedicineException(BusinessRuleException):
    default_detail = 'Expired medicines cannot be sold.'
    default_code = 'expired_medicine'


class NegativeStockException(BusinessRuleException):
    default_detail = 'Stock cannot become negative.'
    default_code = 'negative_stock'
