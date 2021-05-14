from app.models import Banner
from django.shortcuts import render
from .models import Banner,Product
# Create your views here.
def index(request):
    banner=[]
    b=list(Banner.objects.all())
    p=Product.objects.filter(Product_display='All')
    p1=Product.objects.filter(Product_display='New_Arrival')
    p2=Product.objects.filter(Product_display='On_Sale')
    p3=Product.objects.filter(Product_display='Upcoming_product')
    banner.append(b[-1].image1)
    banner.append(b[-1].image2)
    banner.append(b[-1].image3)
    context={
        'banner':banner,
        'all':p,
        'new_arrival':p1,
        'on_sale':p2,
        'upcoming_product':p3

    }
    return render(request,'index.html',context)

def loginpage(request):
    return render(request, "login.html")

def singleproduct(request):
    return render(request, 'single-product.html')

def checkout(request):
    return render(request, 'checkout.html')
