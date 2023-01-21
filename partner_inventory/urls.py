from django.urls import path
from .views import RegisterView, ListCreateInventoryAPIView, RetrieveUpdateDestroyInventoryAPIView, \
    ListCreateProductAPIView, RetrieveUpdateDestroyProductAPIView, UpdatePartnerView, ListCreateListingView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user_details/<uuid>/', UpdatePartnerView.as_view(), name='user_info_update'),
    path('inventory/', ListCreateInventoryAPIView.as_view(), name='get_post_inventory_items'),
    path('inventory/<int:pk>/', RetrieveUpdateDestroyInventoryAPIView.as_view(), name='get_delete_update_inventory_items'),
    path('product/', ListCreateProductAPIView.as_view(), name='get_post_products'),
    path('product/<int:pk>/', RetrieveUpdateDestroyProductAPIView.as_view(), name='get_delete_update_products'),
    path('listing/', ListCreateListingView.as_view(), name='get_post_listing'),
]