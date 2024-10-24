from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Extended Version of PageNumberPagination"""

    page_size = 10
    max_page_size = 100
    page_query_param = "page"
