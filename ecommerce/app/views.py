from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, WishList, Cart, Category, Comment, OrderItem, CartItem, WishItem
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, CommentSerializer, OrderItemSerializer, CardSerializer, CartItemSerializer, WishItemSerializer, CategorySerializer
# from .permissions import IsManager, IsOwnerOrManager
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from django.core.paginator import Paginator,EmptyPage



@api_view(['GET'])
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)

@api_view(['GET'])
def create_checkout_session(request):
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        order = Order.objects.all().last()
        total_amoun = order.total_price
        total_amount=int(total_amoun)*100
        checkout_session = stripe.checkout.Session.create(
            success_url='http://localhost:5173/sec?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5173/fail',
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Total Order Payment',
                        },
                        'unit_amount': total_amount,  # Total amount in cents
                    },
                    'quantity': 1,
                },
            ]
        )
        return Response({'sessionId': checkout_session['id']}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        # Verify the webhook signature and construct the event
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']  # Contains a Stripe payment intent
            # Fulfill the purchase
            print(f"PaymentIntent was successful for {payment_intent['id']}")

        # Other event types can be handled here

        return Response(status=200)

    except ValueError as e:
        # Invalid payload
        return Response({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response({'error': 'Invalid signature'}, status=400)
    except Exception as e:
        # General error handler
        return Response({'error': str(e)}, status=400)



































# Product Views
@api_view(['POST'])
def product_create(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()

    # Apply filters
    min_price = request.query_params.get('min')
    max_price = request.query_params.get('max')
    in_stock = request.query_params.get('in_stock')
    category = request.query_params.get('category')
    is_best = request.query_params.get('is_best')
    fea = request.query_params.get('featured')
    lat = request.query_params.get('latest')
    color = request.query_params.get('color')
    size = request.query_params.get('size')

    perpage = request.query_params.get('perpage', default=2)
    page = request.query_params.get('page', default=1)

    search = request.query_params.get('search')


    if color is not None:
        products = products.filter(available_colors__icontains= color)

    if size is not None:
        products = products.filter(available_sizes__icontains= size)

    if category is not None:
        products = products.filter(category=category)  # Corrected: '=' instead of '=='

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    if in_stock is not None:
        in_stock = in_stock.lower() in ['true', '1', 'yes']
        products = products.filter(stock_status=in_stock)

    if is_best is not None:
        if is_best == 'true':
            products = products.filter(best=True)

    if lat is not None:
        if lat == 'true':
            products = products.order_by('-id')[:4]

    if fea is not None:
        if fea == 'true':
            products = products.filter(featured=True)

    if search is not None:
        products = products.filter(name__icontains= search)



    paginator = Paginator(products,per_page=perpage)
    try:
        products = paginator.page(number=page)
    except EmptyPage:
        products=[]


    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_list_Count(request):
    products = Product.objects.all()

    # Apply filters
    min_price = request.query_params.get('min')
    max_price = request.query_params.get('max')
    in_stock = request.query_params.get('in_stock')
    category = request.query_params.get('category')
    is_best = request.query_params.get('is_best')
    fea = request.query_params.get('featured')
    lat = request.query_params.get('latest')
    color = request.query_params.get('color')
    size = request.query_params.get('size')
    search = request.query_params.get('search')


    if color is not None:
        products = products.filter(available_colors__icontains= color)

    if size is not None:
        products = products.filter(available_sizes__icontains= size)

    if category is not None:
        products = products.filter(category=category)  # Corrected: '=' instead of '=='

    if min_price is not None:
        products = products.filter(price__gte=min_price)

    if max_price is not None:
        products = products.filter(price__lte=max_price)

    if in_stock is not None:
        in_stock = in_stock.lower() in ['true', '1', 'yes']
        products = products.filter(stock_status=in_stock)

    if is_best is not None:
        if is_best == 'true':
            products = products.filter(best=True)

    if lat is not None:
        if lat == 'true':
            products = products.order_by('-id')[:4]

    if fea is not None:
        if fea == 'true':
            products = products.filter(featured=True)

    if search is not None:
        products = products.filter(name__icontains= search)



    serializer = ProductSerializer(products, many=True)
    return Response(len(serializer.data))


@api_view(['PUT'])
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['DELETE'])
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#catigory

@api_view(['GET'])
def catigory_list(request):
    catigory = Category.objects.all()
    serializer = CategorySerializer(catigory, many=True)
    return Response(serializer.data)

# 
@api_view(['POST'])
@csrf_exempt
def catigory_create(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def catigory_delete(request, pk):
    try:
        catigory = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        catigory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#order
@api_view(['POST'])
@csrf_exempt
def order_create(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_list(request):
    use_r = request.query_params.get('user')
    if use_r is not None:
        order =  Order.objects.filter(user=use_r)
    else:
        order = Order.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def order_update(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])
def order_delete(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





#comment
@api_view(['POST'])
def comment_create(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def comment_create(request):
#     if request.method == 'POST':
        
        
        
#         try:
#             rating_ = request.data.get('rating')
#             comment_ = request.data.get('comment')
#             usera = request.data.get('user')
#             product_ = request.data.get('product')
#             comment_item = Comment.objects.filter(product=product_,user=usera)
#             if comment_item:
#                 comment_item.rating=rating_
#                 comment_item.comment=comment_
#                 comment_item.save()
#                 serializer = CommentSerializer(comment_item)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 serializer = CommentSerializer(data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#         except Product.DoesNotExist:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET'])
def comment_list(request):
    comment = Comment.objects.all()
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def comment_update(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(['DELETE'])
def comment_delete(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#orderItem
@api_view(['POST'])
def orderItem_create(request):
    if request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def orderItem_list(request):
    ord = request.query_params.get('ord')
    if ord is not None:
        orderItem =  OrderItem.objects.filter(order=ord)
    else:
        orderItem = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItem, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def orderItem_update(request, pk):
    try:
        orderItem = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OrderItemSerializer(orderItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def orderItem_detail(request, pk):
    try:
        orderItem = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderItemSerializer(orderItem)
    return Response(serializer.data)

@api_view(['DELETE'])
def orderItem_delete(request, pk):
    try:
        orderItem = OrderItem.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        orderItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# card Views
@api_view(['POST'])
def card_create(request):
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def card_list(request):
    card = Cart.objects.all()
    serializer = CardSerializer(card, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def card_update(request, pk):
    try:
        card = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def card_detail(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CardSerializer(cart)
    return Response(serializer.data)

@api_view(['DELETE'])
def card_delete(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# cardItem Views
@api_view(['POST'])
def cardItem_create(request):
        try:
                product_id = request.data.get('product')
                cart_id = request.data.get('cart')
                quantity = request.data.get('quantity')

                cart_item = CartItem.objects.filter(product=product_id, cart=cart_id).first()

                if cart_item:
                    # If the item exists, update the quantity
                    cart_item.quantity += int(quantity)
                    cart_item.save()
                    serializer = CartItemSerializer(cart_item)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    # If the item doesn't exist, create a new one
                    serializer = CartItemSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def cardItem_list(request):
    cardItem = CartItem.objects.all()


    user = request.query_params.get('user')


    if user is not None:
        # cardItem=cardItem
        cardItem = cardItem.filter(cart=user )



    serializer = CartItemSerializer(cardItem, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def cardItem_update(request, pk):
    try:
        cardItem = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CartItemSerializer(cardItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cardItem_detail(request, pk):
    try:
        cardItem = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CartItemSerializer(cardItem)
    return Response(serializer.data)

@api_view(['DELETE'])
def cardItem_delete(request, pk):
    try:
        cardItem = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        cardItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# WhishItem Views
@api_view(['POST'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
def wishItem_create(request):

    product_id = request.data.get('product')
    user_id = request.data.get('user')


    cart_item = WishItem.objects.filter(product=product_id, user=user_id).first()
    if cart_item:
        return Response('alredy exist',status=status.HTTP_201_CREATED)

    
    if request.method == 'POST':
        serializer = WishItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET'])
# def wishItem_list(request):
#     use_r = request.query_params.get('user')
#     print(use_r)
#     orde_r = Order.objects.filter(user=use_r).first()
#     if orde_r is None:
#         wishItem = WishItem.objects.all()
#         serializer = WishItemSerializer(wishItem, many=True)
#     else:
#         wishItem = WishItem.objects.filter(user=use_r)

#         #  # Get the list of product IDs from the wishlist items
#         product_ids = wishItem.values_list('product_id', flat=True)
        
#         # # Retrieve the products associated with those IDs
#         product = Product.objects.filter(id__in=product_ids)
#         # wish=wishItem.id
#         # product =Product.objects.filter(id=wish)
#         serializer = ProductSerializer(product, many=True)
#         print(product)
#     return Response(serializer.data)

@api_view(['GET'])
def wishItem_list(request):
    use_r = request.query_params.get('user')
    print(use_r)
    
    # Check if the user is provided
    if use_r is None:
        return Response({"error": "User ID not provided"}, status=400)
    
    # Filter wishlist items by user
    wish_items = WishItem.objects.filter(user=use_r)
    
    # If no wish items found, return empty list
    if not wish_items.exists():
        return Response({"message": "No wishlist items found for this user"}, status=404)
    
    # Get the list of product IDs from the wishlist items
    product_ids = wish_items.values_list('product_id', flat=True)
    
    # Retrieve the products associated with those IDs
    products = Product.objects.filter(id__in=product_ids)
    
    # Serialize the products
    # products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data)


@api_view(['PUT'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
def wishItem_update(request, pk):
    try:
        wishItem = WishItem.objects.get(pk=pk)
    except WishItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = WishItemSerializer(WishItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def wishItem_detail(request, pk):
    try:
        wishItem = WishItem.objects.get(pk=pk)
    except WishItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = WishItemSerializer(wishItem)
    return Response(serializer.data)

# @api_view(['DELETE'])
# def wishItem_delete(request, pk):
#     use_r = request.query_params.get('user')
#     if use_r is None:
#         try:
#             wishItem = WishItem.objects.get(id=pk)
#         except WishItem.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         if request.method == 'DELETE':
#             wishItem.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
        
#         try:
#             wishItem = WishItem.objects.filter(user=use_r and product=pk)
#         except WishItem.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         if request.method == 'DELETE':
#             wishItem.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)







@api_view(['DELETE'])
def wishItem_delete(request, pk):
    use_r = request.query_params.get('user')

    try:
        if use_r is None:
            # If no user is specified, delete the WishItem by ID
            # wishItem = WishItem.objects.get(id=pk)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # If a user is specified, delete WishItem(s) by user and product ID
            wishItem = WishItem.objects.get(user=use_r, product=pk)
            # if not wishItem.exists():
                

    except WishItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        # Delete the wish item(s)
        wishItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












# Wishlist Views

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def wishlist(request):
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        products = wishlist.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            wishlist.products.add(product)
            return Response(status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def wishlist_remove(request, pk):
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    try:
        product = Product.objects.get(pk=pk)
        wishlist.products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def getProductFromOrder(request):
    use_r = request.query_params.get('user')
    if use_r is not None:
        # Filter the orders by the user
        print(use_r)
        orde_r = Order.objects.filter(user=use_r).first()
        
        if orde_r is None:
            return Response({"detail": "Order not found for the user."}, status=404)
        
        # Get all order items related to the order
        orderItems = OrderItem.objects.filter(order=orde_r)
        
        # Get all products related to these order items
        products = Product.objects.filter(id__in=orderItems.values_list('product_id', flat=True))
        
        # Serialize the products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    return Response({"detail": "User not provided."}, status=400)















# @api_view(['GET'])
# def getProductFromOrder(request):
#     orders = Order.objects.all()
#     products = Product.objects.all()
#     orderItems = OrderItem.objects.all()
#     use_r = request.query_params.get('user')
#     if use_r is not None:
#         orde_r = orders.filter(user=use_r).first()
#         id_order=orde_r.id
#         orderItem = orderItems.filter(order=id_order)
#         order_product=orderItem.product
#         product = products.filter(id=order_product)

#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)
    
