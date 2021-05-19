from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
app_name="app"
urlpatterns = [
   
    path('<int:prid>', views.singleproduct, name="single-product"),
    path('',views.IndexView.as_view(), name="index"),
    path('add_wishlist/<int:pk>', views.add_to_wishlist),
    path('remove_wishlist/<int:pk>', views.remove_from_wishlist),
    path('remove_table_wishlist/<int:pk>', views.remove_from_table_wishlist),
    path('wishlist/', views.WishlistView.as_view(),name='wishlist'),
    path('single-product', views.singleproduct),
    path('checkout', views.checkout),
    path('cart', views.cart,name='cart'),
    #path('checkout', login_required(views.checkoutview.as_view(success_url= ''))),
    path('contact', views.contact,name='contact')
]