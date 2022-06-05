from django.urls import path
from .views import RegisterView, ListCreateInventoryAPIView, RetrieveUpdateDestroyInventoryAPIView, \
    ListCreateProductAPIView, RetrieveUpdateDestroyProductAPIView, RetrieveUpdateDestroyPartnerAPIView, \
    ListPartnerAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('inventory/', ListCreateInventoryAPIView.as_view(), name='get_post_inventory_items'),
    path('inventory/<int:pk>/', RetrieveUpdateDestroyInventoryAPIView.as_view(), name='get_delete_update_inventory_items'),
    path('product/', ListCreateProductAPIView.as_view(), name='get_post_products'),
    path('product/<int:pk>/', RetrieveUpdateDestroyProductAPIView.as_view(), name='get_delete_update_products'),
    path('partner/', ListPartnerAPIView.as_view(), name='get_partner_details'),
    path('partner/<int:pk>/', RetrieveUpdateDestroyPartnerAPIView.as_view(), name='get_delete_update_partner_details'),
]
