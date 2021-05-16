from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.auth.decorators import login_required

urlpatterns = [
   
    path('',views.index, name="index"),
    path('wishlist/<int:pk>', views.add_to_wishlist),
    path('wishlist/', views.wishlist),
    path('single-product', views.singleproduct),
    path('checkout', login_required(views.checkoutview.as_view(success_url= '')))
]