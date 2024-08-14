from rest_framework import serializers
from .models import Product, Comment, Order, WishList, Cart, OrderItem, CartItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'product','user','comment','rating']

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'category', 'quantity', 'price', 'average_rating', 'comments', 'available_colors', 'available_sizes', 'stock_status']

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
        fields = ['id', 'user', 'address', 'total_price', 'tel', 'email', 'date']

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['id', 'user', 'products']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

class CardSerializer(serializers.ModelSerializer):
    # cardIteam = CartItemSerializer(many = True)
    class Meta:
        model = Cart
        fields = ['id', 'user']