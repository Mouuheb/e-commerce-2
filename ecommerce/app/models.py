from django.conf import settings
from django.db import models
# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Ensure superuser is_active is True and is_staff is True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure the superuser must have a password
        if password is None:
            raise ValueError('Superusers must have a password.')

        return self.create_user(email, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.PositiveIntegerField()
    best = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='email')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 rating


    def __str__(self):
        return f'Comment by {self.user.email} on {self.product.name}'
    
    class Meta:
        unique_together = ['product', 'user']  # Ensure a user can only comment once per product

# Order Model
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='email')
    # products = models.ManyToManyField(Product, through='OrderItem')
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tel = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='Processing',max_length=255)
    # orderItems = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f'Order {self.id} by {self.user.email}'

# OrderItem Model to link Product and Order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in order {self.order.id}'

# WishList Model
class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='email')
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f'Wishlist of {self.user.email}'

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='email')
    # products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart of {self.user.email}'
    
    class Meta:
        unique_together = ['user']

# CartItem Model to link Product and Cart
class CartItem(models.Model):
    cart = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='email')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    available_colors = models.JSONField(default=list)
    available_sizes = models.JSONField(default=list)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in cart {self.cart.id}'

class WishItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='email')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} hope {self.product.name}'

