from rest_framework import serializers
from .models import Product, Comment, Order, WishList, Cart, OrderItem, CartItem

class ProductSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'category', 'quantity', 'price', 'rate', 'comments', 'available_colors', 'available_sizes', 'stock_status']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'address', 'total_price', 'tel', 'email']
