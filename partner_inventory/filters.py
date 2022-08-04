from django_filters import rest_framework as filters
from .models import Inventory


# We create filters for each field we want to be able to filter on
class InventoryFilter(filters.FilterSet):
    product = filters.CharFilter(lookup_expr='icontains')
    partner = filters.CharFilter(lookup_expr='icontains')
    available = filters.NumberFilter()
#    created_at = filters.DateRangeFilter(lookup_expr='')
#    updated_at = filters.DateRangeFilter(lookup_expr='lt')

    class Meta:
        model = Inventory
        fields = ['product', 'partner', 'available', 'created_at', 'updated_at']

