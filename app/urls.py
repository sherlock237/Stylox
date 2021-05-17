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
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('add_wishlist/<int:pk>', views.add_to_wishlist),
    path('remove_wishlist/<int:pk>', views.remove_from_wishlist),
    path('remove_table_wishlist/<int:pk>', views.remove_from_table_wishlist),
    path('wishlist/', views.WishlistView.as_view(),name='wishlist'),
    path('single-product', views.singleproduct),
    path('checkout', login_required(views.checkoutview.as_view(success_url= ''))),
    path('contact', views.contact,name='contact')
]