from rest_framework import serializers
from .models import Product, Comment, Order, WishList, Cart, OrderItem, CartItem, Category, WishItem

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'product','user','comment','rating']

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'category', 'quantity', 'price', 'sold', 'average_rating', 'comments', 'available_colors', 'available_sizes', 'stock_status', 'featured', 'best']

    def get_average_rating(self, obj):
        return obj.average_rating()

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    # orderItem = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'total_price', 'tel', 'email', 'date', 'status']

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['id', 'user', 'products']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'available_colors', 'available_sizes']

class CardSerializer(serializers.ModelSerializer):

    # cardIteam = CartItemSerializer(many = True)
    class Meta:
        model = Cart
        fields = ['id', 'user']

class WishItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishItem
        fields = ['id', 'user', 'product']