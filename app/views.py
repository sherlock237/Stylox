from app.models import Banner
from django.shortcuts import render
from .models import Banner,Product, Checkout, Wishlist, MyProfile,Subscribe
from django.views.generic.edit import CreateView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

def demo(email):
    if(User.objects.filter(email=email)):
        sub=Subscribe(email=email,our_user=True)
        sub.save()
    else:
        sub=Subscribe(email=email,our_user=False)
        sub.save() 


def index(request):
    if request.method =='POST' and request.POST['action']=='subs':
        email=request.POST.get('email')
        if(Subscribe.objects.filter(email=email)):
            messages.error(request,'Already subscribed')
        else:
            demo(email)
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

def singleproduct(request,prid): 
    prd=Product.objects.filter(prid=prid)
    size=0
    for i in prd:
        size=i.size_available
        break
    size=size.split(',')
    context={
        'prd':prd,
        'size':size
    }
    return render(request, 'single-product.html',context)


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

@login_required
def add_to_wishlist(req, pk):
    product = Product.objects.get(pk=pk)
    cuser, created = MyProfile.objects.get_or_create(user=req.user)
    Wishlist.objects.create(product = product, current_user = cuser )
    return HttpResponseRedirect(redirect_to="/wishlist")


@login_required()
def wishlist(request):
    #add_to_wishlist(request,pk)
    #product = Wishlist.objects.filter(current_user = pk)
    #product_details = Product.objects.filter()
    return render(request, 'wishlist.html')






