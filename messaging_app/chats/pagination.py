# messaging_app/chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    20 results per page by default.
    Clients can override with ?page_size=<n> up to max_page_size.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
