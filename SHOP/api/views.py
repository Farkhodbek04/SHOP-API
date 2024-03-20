from main import models
from . import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def all_products(request):
    if request.method == 'GET':
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, id):
    if request.method == 'GET':
        try:
            product = models.Product.objects.get(id=id)
            serializer = serializers.ProductSerializer(product)
            images = models.ProductImages.objects.filter(product=product)
            image_serializer = serializers.ProductImageSerializer(images, many=True)
            serialized_data = serializer.data  # Get the serialized data of the product
            serialized_data['images'] = image_serializer.data  # Add the images data to the serialized data
            return Response(serialized_data)
        except models.Product.DoesNotExist: 
            return Response( {'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
def add_to_wishlist(request, id):
    if request.method == "POST":
        user = request.user
        try:
            product = models.Product.objects.get(id=id)
        except models.Product.DoesNotExist: 
            return Response( {'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            models.Wishlist.objects.get(product=product, user=user)
            message = 'Product has been removed from your wishlist.'
        except models.Wishlist.DoesNotExist:  
            message = 'Product has been added to your wishlist'
        models.Wishlist.objects.create(
            user = user,
            product = product
        )
        return Response({'message': message})
    
@api_view(['POST'])
def give_review(request, id):
    if request.method == 'POST':
        user = request.user
        try:
            product = models.Product.objects.get(id=id)
        except models.Product.DoesNotExist:
            return Response({'message': 'Product not found!'})
        try: 
            models.ProductReview.objects.get(user=user, product=product)
            message = "Your review has been updated."
        except models.ProductReview.DoesNotExist:
            message = 'Your review have been accepted.'
        models.ProductReview.objects.create(
            user = user,
            product = product,
            mark = request.data.get('mark')
        )
        return Response({'message':message})

@api_view(['POST'])
def add_to_cart(request, id):
    if request.method == 'POST':
        try:
            cart = models.Cart.objects.get(user=request.user, is_active=True)
        except models.Cart.DoesNotExist:
            models.Cart.objects.create(user=request.user, is_active=True)
            cart = models.Cart.objects.get(user=request.user, is_active=True)
        models.CartProduct.objects.create(associated_cart=cart, product = id)
        return Response({'message':'The product has been added to your Cart.'})
    
@api_view(['GET'])
def cart_detail(request):
    if request.method == 'GET':
        try:
            cart = models.Cart.objects.get(user=request.user, is_active=True)
            serializer = serializers.CartSerializer(cart)
            return Response(serializer.data)
        except models.Cart.DoesNotExist:
            return Response({'Cart not found.'})
        
@api_view(['POST'])
def remove_from_cart(request, id):
    if request.method == 'POST':
        try:
            product = models.Product.objects.get(id=id)
            cart = models.Cart.objects.get(user=request.user, is_active=True)
            cart_product = models.CartProduct.objects.get(product=product, associated_cart=cart)
            cart_product.delete()
            return Response({'message':'Product deleted!'})
        except models.Product.DoesNotExist:
            return Response({'message':'Product not found'})
        
@api_view(['POST'])
def order(request):
    cart = models.Cart.objects.get(user=request.user, is_active=True)
    models.Order.objects.create(
        cart=cart,
        user=request.user)
    cart.is_active =False
    cart.save()
    return Response({'message': 'Your order has been ordered :)'})
    
    # Auth
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    
    return Response({'message': 'User created successfully', 'token': token.key})
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def logout_user(request):
    token_key = request.data.get('token')
    
    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    token.delete()
    
    return Response({'message': 'Logged out successfully'})

# USER AUTH
# Register -> POST                                  +
# Log in -> POST                                    +
# Log out -> PUT                                    +

# ALL products -> GET                               +
# Product detail -> GET                             +
# Add or Remove Product to wishlsit -> POST         +
# Give Review -> POST                               +
# Add Product to Cart -> POST                       +
# Cart detail                                       +            
# Remove Product from Cart - POST                   +
# Order Cart - POST                                 +
# Cancel Order - POST
