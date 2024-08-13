from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),

    # Order URLs
    path('orders/', views.order_list, name='order-list'),
    path('orders/create/', views.order_create, name='order-create'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),

    # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/<int:pk>/remove/', views.wishlist_remove, name='wishlist-remove'),

    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('cart/<int:pk>/remove/', views.cart_remove, name='cart-remove'),
]
