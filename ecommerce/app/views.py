from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, WishList, Cart
from .serializers import ProductSerializer, OrderSerializer
# from .permissions import IsManager, IsOwnerOrManager


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
    category = request.query_params.get('max_price')

    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)
    if in_stock is not None:
        in_stock = in_stock.lower() in ['true', '1', 'yes']
        products = products.filter(in_stock=in_stock)


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

# Order Views

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def order_create(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
# @permission_classes([IsAuthenticated, IsOwnerOrManager])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
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

# Cart Views

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        cart_items = cart.cartitem_set.all()
        serializer = ProductSerializer([item.product for item in cart_items], many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            cart.products.add(product)
            return Response(status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def cart_remove(request, pk):
    cart, created = Cart.objects.get_or_create(user=request.user)
    try:
        product = Product.objects.get(pk=pk)
        cart.products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

