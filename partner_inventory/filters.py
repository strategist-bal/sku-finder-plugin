from django_filters import rest_framework as filters
from .models import Inventory, Product, Listing
from django.db.models import Q


class ListingFilterSet(filters.FilterSet):
    product_name = filters.CharFilter(method='qfilter')

    class Meta:
        model = Listing
        fields = ['id', 'selling_price', 'partner_id', 'inventory', 'partner']

    def qfilter(self, queryset, name, value):
        squery = Q(inventory__product__name__icontains=value)

        return queryset.filter(squery)


class InventoryFilter(filters.FilterSet):
    product = filters.CharFilter(lookup_expr='icontains')
    partner = filters.CharFilter(lookup_expr='icontains')
    available = filters.NumberFilter()
#    created_at = filters.DateRangeFilter(lookup_expr='')
#    updated_at = filters.DateRangeFilter(lookup_expr='lt')

    class Meta:
        model = Inventory
        fields = ['product', 'partner', 'available', 'created_at', 'updated_at']


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'mrp', 'partner']

