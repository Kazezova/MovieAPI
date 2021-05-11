from django.db.models import F, Value as V
from django.db.models.functions import Concat, Lower

from django_filters import rest_framework as filters
from main.models import Movie


class MovieFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__name', lookup_expr='exact')
    country = filters.CharFilter(field_name='country', lookup_expr='exact')
    release_date = filters.NumberFilter(method='filter_release_date')
    producer = filters.CharFilter(method='filter_producer')
    avg_score = filters.NumberFilter(field_name='avg_score', lookup_expr='gte')

    class Meta:
        model = Movie
        fields = ('genre', 'country', 'release_date', 'producer', 'avg_score')

    def filter_producer(self, queryset, name, value):
        if value:
            queryset = queryset.annotate(
                full_name=Lower(Concat(F('producer__first_name'), V(' '), F('producer__last_name')))).filter(
                full_name__contains=value.lower())
        return queryset

    def filter_release_date(self, queryset, name, value):
        if value:
            queryset = queryset.filter(release_date__year=value)
        return queryset

# class NullsLastOrderingFilter(filters.OrderingFilter):
#     def filter(self, qs, value):
#         if value in ([], (), {}, '', None):
#             return qs
#
#         ordering = [self.get_ordering_value(param) for param in value]
#
#         def filter_object(x):
#             return F(x[1:]).desc(
#                 nulls_last=True
#             ) if x[0] == '-' else F(x).asc(
#                 nulls_last=True
#             )
#
#         if ordering:
#             ordering = map(filter_object, ordering)
#             queryset = qs.order_by(*ordering)
#
#         return queryset
