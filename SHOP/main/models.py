from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import  User

from rest_framework.authtoken.models import Token

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    baner_image = models.ImageField(upload_to='baner_images/')
    quantity = models.IntegerField()

    @property
    def review(self):
        reviews = ProductReview.objects.filter(product=self)
        result = sum([result.mark for result in reviews])
        try:
            result /= reviews.count()
        except ZeroDivisionError:
            result = 0            
        return round(result, 2)
    
    @property
    def review_number(self):
        product_review = ProductReview.objects.filter(product=self)
        return product_review.count()
    
    @property
    def is_active(self):
        return self.quantity > 0
    
    @property
    def discount_price(self):
        if self.is_discount and self.discount_percentage:
            price = self.price - (self.discount_percentage/100*self.price)
            return round(price, 2)

    def __str__(self):
        return self.title
    

class ProductImages(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} image'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} - {self.product}'
    
    def save(self, *args, **kwargs):
        try:
            object = Wishlist.objects.get(product=self.product, user=self.user) 
            object.delete()
        except Wishlist.DoesNotExist:
            super(Wishlist, self).save(*args, **kwargs)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            ProductReview.objects.filter(user=self.user, product=self.product).update(mark=self.mark)
        except ObjectDoesNotExist:
            # If the ProductReview object doesn't exist, proceed with the default save behavior
            super(ProductReview, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}->{self.product}-{self.mark}'
            
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', related_name='cart_items')  # Added related_name
    is_active = models.BooleanField(default=False)

    @property
    def quantity_in_cart(self):
        return self.products.count()

    @property
    def price_in_cart(self):
        total_price = sum(
            product.discount_price if product.is_discount else product.price
            for product in self.products.all()
        )
        return total_price


class CartProduct(models.Model):
    associated_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Renamed field
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    ordered_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    @property
    def is_active(self):
        if self.status == 'Delivered' or self.status == 'Canceled':
            return False
        else: 
            return True
        
    # def save(self, *args, **kwargs):
    #     if self.status == 'Delivered':
    #         ...

