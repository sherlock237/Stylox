from app.models import Banner
from django.shortcuts import render
from .models import Banner,Product, Checkout, User
from django.views.generic.edit import CreateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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

def register(request):
    return render(request, "register.html")

def singleproduct(request):
    return render(request, 'single-product.html')


def checkout(request):
    return render(request, 'checkout.html')

@method_decorator(login_required, name='dispatch')
class checkoutview(CreateView):
    model = Checkout
    fields = ['fname', 'lname', 'company', 'address' , 'state', 'city', 'zip_code', 'address', 'phone' , 'add_info']

    def form_valid(self, form):
        self.object = form.save()
        self.object.check_id = self.request.user
        self.object.product_id = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url(), 'checkout_form.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'

def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'accounts/index.html')
    context['form']=form
    return render(request,'registration/sign_up.html',context)

def logout(request):
    return render(request, 'registration/logout.html')

