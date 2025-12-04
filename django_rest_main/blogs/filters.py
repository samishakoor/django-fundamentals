import django_filters
from .models import Blog


class BlogFilter(django_filters.FilterSet):
    blog_title = django_filters.CharFilter(
        field_name="blog_title", lookup_expr="iexact"
    )
    blog_body = django_filters.CharFilter(field_name="blog_body", lookup_expr="icontains")
    id_min = django_filters.CharFilter(method='filter_by_id_range', label='From BLOG ID')
    id_max = django_filters.CharFilter(method='filter_by_id_range', label='To BLOG ID')

    class Meta:
        model = Blog
        fields = ["blog_title", "blog_body", 'id_min', 'id_max']

    def filter_by_id_range(self, queryset, name, value):
        if name == 'id_min':
            return queryset.filter(id__gte=value)
        elif name == 'id_max':
            return queryset.filter(id__lte=value)
        return queryset