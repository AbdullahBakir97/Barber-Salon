from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 10