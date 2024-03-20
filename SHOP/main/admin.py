from django.contrib import admin

from . import models

# Register your models here
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductImages)
admin.site.register(models.ProductReview)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.Wishlist)
admin.site.register(models.Order)

