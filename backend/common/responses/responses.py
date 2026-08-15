"""
Standard API response helpers.
Ensures every response follows:
{
    "success": true/false,
    "message": "...",
    "data": {}
}
"""

from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message='Success', status_code=status.HTTP_200_OK):
    """Return a standard success response."""
    return Response(
        {
            'success': True,
            'message': message,
            'data': data or {},
        },
        status=status_code,
    )


def created_response(data=None, message='Created successfully.'):
    """Return a standard 201 response."""
    return success_response(data=data, message=message, status_code=status.HTTP_201_CREATED)


def error_response(message='An error occurred.', errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Return a standard error response."""
    return Response(
        {
            'success': False,
            'message': message,
            'errors': errors or {},
        },
        status=status_code,
    )


def no_content_response():
    """Return a 204 No Content response (e.g., soft delete)."""
    return Response(status=status.HTTP_204_NO_CONTENT)
