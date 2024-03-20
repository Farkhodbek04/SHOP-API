from rest_framework import serializers
from main import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.User
        fields = ['phone_number', 'avatar', 'first_name', 'last_name', 'email', 'data_joined', '']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_images(self, obj):
    # Retrieve and serialize related images for the product
        images = models.ProductImages.objects.filter(product=obj)
        serializer = ProductImageSerializer(images, many=True)
        return serializer.data

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartProduct
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = models.Cart
        fields = '__all__'

    def get_products(self, obj):
        # Retrieve and serialize related products for the cart
        products = models.CartProduct.objects.filter(associated_cart=obj)
        serializer = CartProductSerializer(products, many=True)
        return serializer.data
















































































































































































































































































































































