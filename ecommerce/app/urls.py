from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('productsCount/', views.product_list_Count, name='product-list'),

    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),

    # Catigory URLs
    path('catigory/create/', views.catigory_create, name='catigory-create'),
    path('catigory/<int:pk>/delete/', views.catigory_delete, name='catigory-delete'),
    path('catigory/', views.catigory_list, name='catigory-list'),

    # Order URLs
    path('order/', views.order_list, name='order-list'),
    path('order/<int:pk>/', views.order_detail, name='order-detail'),
    path('order/create/', views.order_create, name='order-create'),
    path('order/<int:pk>/update/', views.order_update, name='order-update'),
    path('order/<int:pk>/delete/', views.order_delete, name='order-delete'),

    # comment URLs
    path('comment/', views.comment_list, name='comment-list'),
    path('comment/<int:pk>/', views.comment_detail, name='comment-detail'),
    path('comment/create/', views.comment_create, name='comment-create'),
    path('comment/<int:pk>/update/', views.comment_update, name='comment-update'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),

    # orderItem URLs
    path('orderItem/', views.orderItem_list, name='orderItem-list'),
    path('orderItem/<int:pk>/', views.orderItem_detail, name='orderItem-detail'),
    path('orderItem/create/', views.orderItem_create, name='orderItem-create'),
    path('orderItem/<int:pk>/update/', views.orderItem_update, name='orderItem-update'),
    path('orderItem/<int:pk>/delete/', views.orderItem_delete, name='orderItem-delete'),

    # card URLs
    path('card/', views.card_list, name='card-list'),
    path('card/<int:pk>/', views.card_detail, name='card-detail'),
    path('card/create/', views.card_create, name='card-create'),
    path('card/<int:pk>/update/', views.card_update, name='card-update'),
    path('card/<int:pk>/delete/', views.card_delete, name='card-delete'),

    # cardItem URLs
    path('cardItem/', views.cardItem_list, name='cardItem-list'),
    path('cardItem/<int:pk>/', views.cardItem_detail, name='cardItem-detail'),
    path('cardItem/create/', views.cardItem_create, name='cardItem-create'),
    path('cardItem/<int:pk>/update/', views.cardItem_update, name='cardItem-update'),
    path('cardItem/<int:pk>/delete/', views.cardItem_delete, name='cardItem-delete'),

    # WishItem URLs
    path('wishItem/', views.wishItem_list, name='wishItem-list'),
    path('wishItem/<int:pk>/', views.wishItem_detail, name='wishItem-detail'),
    path('wishItem/create/', views.wishItem_create, name='wishItem-create'),
    path('wishItem/<int:pk>/update/', views.wishItem_update, name='wishItem-update'),
    path('wishItem/<int:pk>/delete/', views.wishItem_delete, name='wishItem-delete'),


    path('config/', views.stripe_config),  # new
    path('create-checkout-session/', views.create_checkout_session), # new
    #path('success/', views.SuccessView.as_view()), # new
    #path('cancelled/', views.CancelledView.as_view()), # new
    path('webhook/', views.stripe_webhook), # new


    path('getProductFromOrder/', views.getProductFromOrder, name='getProductFromOrder'),



]
