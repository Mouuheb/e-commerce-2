from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    stock_status = models.BooleanField(default=True)  # True for in stock, False for out of stock

    # rate_quantity = models.PositiveIntegerField()

    # Additional Fields
    available_colors = models.JSONField(default=list)
    available_sizes = models.JSONField(default=list)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = [comment.rating for comment in self.comments.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        return 0.0

# Comment Model
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    #rating = models.IntegerField()  # 1-5 rating
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 rating


    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.name}'
    
    class Meta:
        unique_together = ['product', 'user']  # Ensure a user can only comment once per product

# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # products = models.ManyToManyField(Product, through='OrderItem')
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tel = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# OrderItem Model to link Product and Order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in order {self.order.id}'

# WishList Model
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f'Wishlist of {self.user.username}'

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart of {self.user.username}'
    
    class Meta:
        unique_together = ['user']

# CartItem Model to link Product and Cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in cart {self.cart.id}'

