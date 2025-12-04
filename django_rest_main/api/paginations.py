from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "per_page"
    page_query_param = "page"
    max_page_size = 10  # maximum items a client can request, if we specify per_page param in query, then its maximum value can be 10
    page_size = 10  # default page size, if we don't specify per_page param in query then by default, each page will have 5 items

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "page_size": self.page_size,
                "results": data,
            }
        )
