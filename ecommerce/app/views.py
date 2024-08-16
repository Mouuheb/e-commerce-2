from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, WishList, Cart, Category, Comment, OrderItem, CartItem, WishItem
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, CommentSerializer, OrderItemSerializer, CardSerializer, CartItemSerializer, WishItemSerializer
# from .permissions import IsManager, IsOwnerOrManager
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Product Views
@api_view(['POST'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    in_stock = request.query_params.get('in_stock')
    category = request.query_params.get('category')
    is_best = request.query_params.get('is_best')

    fea = request.query_params.get('featured')
    lat = request.query_params.get('latest')

    if category is not None:
        products = products.filter(price__gte=category)
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
        # products = []
        if fea == 'true':
            products = products.filter(featured=True)


    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#catigory


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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
    order = Order.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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

@api_view(['GET'])
def comment_list(request):
    comment = Comment.objects.all()
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
def orderItem_create(request):
    if request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def orderItem_list(request):
    orderItem = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItem, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
def cardItem_create(request):
    try:
        # Extracting product and cart from the request data
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

# def cardItem_create(request):
#     if request.method == 'POST':
#         try:
#             cardItem = CartItem.objects.get(product=request.product,cart=request.cart)
#             if cardItem != None and cardItem !=[]:
#                 pk=cardItem.id
#                 request={
#                     "id":pk,
#                     "card":cardItem.cart,
#                     "product":cardItem.product,
#                     "quantity":(cardItem.quantity+request.quantity)
#                 }
#                 cardItem_update(request, pk)
#                 pass
#         except CartItem.DoesNotExist:
#             pass
#         serializer = CartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def cardItem_list(request):
    cardItem = CartItem.objects.all()
    serializer = CartItemSerializer(cardItem, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
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
    if request.method == 'POST':
        serializer = WishItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def wishItem_list(request):
    wishItem = WishItem.objects.all()
    serializer = CartItemSerializer(wishItem, many=True)
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

@api_view(['DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly, IsManager])
def wishItem_delete(request, pk):
    try:
        wishItem = WishItem.objects.get(pk=pk)
    except WishItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
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