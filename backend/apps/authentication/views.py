"""
Authentication Views.
Views are thin — they only validate input, call service, return response.
No business logic here.
"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from common.responses.responses import success_response, error_response
from .serializers import LoginSerializer, TokenRefreshInputSerializer, UserSerializer
from .services.auth_service import AuthService


class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Public endpoint — no authentication required.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description='Login successful. Returns access + refresh tokens.'),
            401: OpenApiResponse(description='Invalid credentials.'),
        },
        summary='Login',
        description='Authenticate with username and password. Returns JWT access and refresh tokens.',
        tags=['Authentication'],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            result = AuthService.login(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            return success_response(data=result, message='Login successful.')
        except ValueError as exc:
            return error_response(message=str(exc), status_code=401)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Requires authentication. Blacklists refresh token.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={'application/json': {'type': 'object', 'properties': {'refresh': {'type': 'string'}}}},
        responses={
            200: OpenApiResponse(description='Logged out successfully.'),
            400: OpenApiResponse(description='Invalid token.'),
        },
        summary='Logout',
        description='Blacklist the refresh token. Frontend should also remove stored tokens.',
        tags=['Authentication'],
    )
    def post(self, request):
        refresh_token = request.data.get('refresh', '').strip()
        if not refresh_token:
            return error_response(
                message='Refresh token is required.',
                status_code=400,
            )

        try:
            AuthService.logout(refresh_token)
            return success_response(message='Logged out successfully.')
        except ValueError as exc:
            return error_response(message=str(exc), status_code=400)


class TokenRefreshView(APIView):
    """
    POST /api/v1/auth/refresh/
    Public endpoint — takes refresh token, returns new access token.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=TokenRefreshInputSerializer,
        responses={
            200: OpenApiResponse(description='New access token returned.'),
            401: OpenApiResponse(description='Invalid or expired refresh token.'),
        },
        summary='Refresh Token',
        description='Exchange a valid refresh token for a new access token.',
        tags=['Authentication'],
    )
    def post(self, request):
        serializer = TokenRefreshInputSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            result = AuthService.refresh_token(
                refresh_token_str=serializer.validated_data['refresh']
            )
            return success_response(data=result, message='Token refreshed successfully.')
        except ValueError as exc:
            return error_response(message=str(exc), status_code=401)


class MeView(APIView):
    """
    GET /api/v1/auth/me/
    Returns current authenticated user's info.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description='Authentication required.'),
        },
        summary='Current User',
        description='Returns information about the currently authenticated user.',
        tags=['Authentication'],
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(
            data=serializer.data,
            message='User details fetched successfully.',
        )
