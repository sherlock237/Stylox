from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('',views.IndexView.as_view(), name="index"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('add_wishlist/<int:pk>', views.add_to_wishlist),
    path('remove_wishlist/<int:pk>', views.remove_from_wishlist),
    path('wishlist/', views.WishlistView.as_view()),
    path('single-product', views.singleproduct),
    path('checkout', login_required(views.checkoutview.as_view(success_url= ''))),
    path('contact', views.contact)
]