from django.urls import path
from .views import GoogleView, ListProductAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/google/', GoogleView.as_view(), name='google_auth'),
    path('product/', ListProductAPIView.as_view(), name='get_post_products'),
]