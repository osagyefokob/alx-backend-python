# messaging_app/messaging_app/settings.py
# add or update this REST_FRAMEWORK block

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # default pagination class for the project
    "DEFAULT_PAGINATION_CLASS": "chats.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
    # filtering backends (django-filter is required)
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
}
