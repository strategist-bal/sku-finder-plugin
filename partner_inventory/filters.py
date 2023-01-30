from django_filters import rest_framework as filters
from .models import Inventory, Product
from django.db.models import Q


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'mrp', 'partner']


class InventoryFilter(filters.FilterSet):
    product = ProductFilter()
    partner = filters.CharFilter(lookup_expr='icontains')
    available = filters.NumberFilter()
#    created_at = filters.DateRangeFilter(lookup_expr='')
#    updated_at = filters.DateRangeFilter(lookup_expr='lt')

    class Meta:
        model = Inventory
        fields = ['product', 'partner', 'available', 'created_at', 'updated_at']

