from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.auth.decorators import login_required
app_name="app"

urlpatterns = [
    path('accounts/logout/', views.logout,name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login', views.loginpage, name="login"),
    path('<int:prid>', views.singleproduct, name="single-product"),
    path('checkout',views.checkout,name='checkout'),
    path('register', views.register, name="register"),
    path('wishlist/<int:pk>', views.add_to_wishlist),

    path('',views.IndexView.as_view(), name="index"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('add_wishlist/<int:pk>', views.add_to_wishlist),
    path('remove_wishlist/<int:pk>', views.remove_from_wishlist),
    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('single-product', views.singleproduct),
    path('checkout', login_required(views.checkoutview.as_view(success_url= ''))),
    path('contact', views.contact,name='contact')
]