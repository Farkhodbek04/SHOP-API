from . import views

from django.urls import path


urlpatterns = [
    path('all-products', views.all_products),
    path('product-detail/<int:id>', views.product_detail),
    path('wishlist/<int:id>', views.add_to_wishlist),
    path('give-review/<int:id>', views.give_review),
    path('add-to-cart/<int:id>', views.add_to_cart),
    path('cart-detail/', views.cart_detail),
    path('remove-from-cart', views.remove_from_cart),
    path('order', views.order),
    # Auth
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
]