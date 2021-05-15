from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
   
    path('',views.index, name="index"),
    path('login', views.loginpage, name="login"),
    path('<int:prid>', views.singleproduct, name="single-product"),
    path('checkout',views.checkout )
]