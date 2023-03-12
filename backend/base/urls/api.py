from rest_framework.routers import DefaultRouter
from ..views.product_views import API

router = DefaultRouter()

router.register('api', viewset=API)

urlpatterns = router.urls