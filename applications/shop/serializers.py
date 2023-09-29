from rest_framework import serializers

from .models import Category, Product, OrderItem, ShippingAddress, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'description', 'price', 'stock', 'image_url')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity')


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('id', 'type', 'address', 'city', 'state', 'zipcode')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = ('id', 'transaction_id', 'items', 'shipping_address', 'date_ordered', 'is_ordered', 'date_delivered',
                  'is_delivered', 'date_cancelled', 'is_cancelled')
