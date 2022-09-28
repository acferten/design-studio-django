import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        exclude = ('name', 'description', 'plan', 'design', 'orderer', 'category', 'date')


class AllOrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        exclude = ('name', 'description', 'plan', 'design', 'orderer', 'status', 'date')
