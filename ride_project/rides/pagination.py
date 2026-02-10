from rest_framework.pagination import PageNumberPagination


class RidePagination(PageNumberPagination):
    page_size = 20