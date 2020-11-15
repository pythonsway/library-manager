from django_filters import rest_framework as filters

from catalog.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(
        field_name='authors__name', lookup_expr='icontains')
    start_date = filters.NumberFilter(
        field_name='pub_date', lookup_expr='year__gte')
    end_date = filters.NumberFilter(
        field_name='pub_date', lookup_expr='year__lte')
    language = filters.CharFilter(
        field_name='language__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'start_date', 'end_date', 'language']
