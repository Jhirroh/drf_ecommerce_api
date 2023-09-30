from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, OrderItem, ShippingAddress, Order
from .serializers import CategorySerializer, ProductSerializer, OrderItemSerializer, ShippingAddressSerializer, \
    OrderSerializer
from .permissions import AdminCreateUpdateDestroyPermission


class CategoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                      DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                     DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AdminCreateUpdateDestroyPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def perform_create(self, serializer):
        product_data = serializer.validated_data
        category_data = product_data.pop('category', None)

        if category_data:
            category, created = Category.objects.get_or_create(**category_data)
        else:
            raise serializers.ValidationError({'category': ['This field is required.']})

        product_data['category'] = category
        serializer.save()


class OrderItemViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = OrderItemSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user)


class ShippingAddressViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = ShippingAddressSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)


class OrderViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                   DestroyModelMixin):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


