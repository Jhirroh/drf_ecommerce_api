from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, OrderItemViewSet, ShippingAddressViewSet, OrderViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('order-items/', OrderItemViewSet, basename='order-items')
router.register('order', OrderViewSet, basename='order')
router.register('shipping-addresses', ShippingAddressViewSet, basename='shipping-addresses')

urlpatterns = []
urlpatterns += router.urls
