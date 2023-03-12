from django.urls import path
from backend.base.views.product_views import API
from base.views import vendor_views as views


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerVendor, name='register'),
] 
