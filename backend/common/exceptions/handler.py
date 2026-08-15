"""
Custom exception handler for DRF.
Ensures every error response follows the standard format:
{
    "success": false,
    "message": "...",
    "errors": {}
}
"""

import logging

from rest_framework.views import exception_handler
from rest_framework import status

logger = logging.getLogger('apps')


def custom_exception_handler(exc, context):
    """
    Override DRF's default exception handler to return
    the project-standard error response format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'success': False,
            'message': _get_message(response, exc),
            'errors': _get_errors(response),
        }
        response.data = custom_data
    else:
        # Unhandled exception — log it and return 500
        logger.exception(
            f"Unhandled exception in {context.get('view', 'unknown')}: {exc}"
        )

    return response


def _get_message(response, exc):
    """Extract a human-readable top-level message."""
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        return 'Authentication credentials were not provided or are invalid.'
    if response.status_code == status.HTTP_403_FORBIDDEN:
        return 'You do not have permission to perform this action.'
    if response.status_code == status.HTTP_404_NOT_FOUND:
        return 'Requested resource not found.'
    if hasattr(exc, 'detail') and isinstance(exc.detail, str):
        return exc.detail
    return 'Validation failed.'


def _get_errors(response):
    """Extract field-level errors if available."""
    data = response.data
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in ('detail',)}
    if isinstance(data, list):
        return {'non_field_errors': data}
    return {}
