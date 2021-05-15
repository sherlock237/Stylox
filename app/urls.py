from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.auth.decorators import login_required

urlpatterns = [
   
    path('',views.index, name="index"),
    path('accounts/logout/', views.logout),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login', views.loginpage, name="login"),
    path('register', views.register, name="register"),
    path('single-product', views.singleproduct),
    path('checkout', login_required(views.checkoutview.as_view(success_url= '')))
]