from django.views.generic.base import TemplateView
from app.models import Banner
from django.shortcuts import render, redirect
from .models import Banner,Product, Checkout, Wishlist, MyProfile,Subscribe
from django.views.generic.edit import CreateView
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import re
# Create your views here.
    # if request.method =='POST' and request.POST['action']=='subs':
    #     email=request.POST.get('email')
    #     if(Subscribe.objects.filter(email=email)):
    #         messages.error(request,'Already subscribed')
    #     else:
    #         demo(email)
def demo(self,email):
    if(User.objects.filter(email=email)):
        sub=Subscribe(email=email,our_user=True)
        sub.save()
        return "Thank you for subscribing"
    else:
        sub=Subscribe(email=email,our_user=False)
        sub.save()
        print("ree") 
        return "Thank you for subscribing"



@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)  
        productList = Product.objects.all()   
        c_user, created = MyProfile.objects.get_or_create(user=self.request.user)
        
        for p11 in productList:  
            #print(p11)
            p11.wished = False
            ob = Wishlist.objects.filter(product = p11,current_user=c_user)  
            #print("ob", ob)
            if ob: 
                p11.wished = True        
            obList = Wishlist.objects.filter(current_user = self.request.user.myprofile)
            p11.wishedno = obList.count()

        banner=[]
        b=list(Banner.objects.all())
        p=Product.objects.filter(Product_display='All')
        p1=Product.objects.filter(Product_display='New_Arrival')
        p2=Product.objects.filter(Product_display='On_Sale')
        p3=Product.objects.filter(Product_display='Upcoming_product')

  
        #print(p.wished)
        banner.append(b[-1].image1)
        banner.append(b[-1].image2)
        banner.append(b[-1].image3)
        context['banner'] = banner
        context['all'] = p
        context['new_arrival'] = p1
        context['on_sale'] = p2
        context['upcoming_product'] = p3
        context['mywish_list'] = productList

        return context
    def post(self,*args, **kwargs):
        if self.request.method =='POST' and self.request.POST['action']=='subs':
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
            msg=""
            email=self.request.POST.get('email')
            if(email==""):
                msg="Please enter valid email address"
            elif not re.search(regex,email):
                msg="Please enter valid email address"
            elif(Subscribe.objects.filter(email=email)):
                msg='Already subscribed'
               
            else:
                try:
                    msg=demo(self,email)
                except:
                    msg='Unable to Subscribe'
            context={'msg':msg}
            return JsonResponse(context)
        
                
def loginpage(request):
    return render(request, "login.html") 

def contact(request):
    return render(request, 'contact.html')

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
    template_name = 'checkout_form.html'
    model = Checkout
    fields = ['First_Name', 'Last_Name', 'company', 'address' , 'state', 'city', 'zip_code', 'email', 'phone' , 'Additional_information']

    def form_valid(self, form):
        self.object = form.save()
        self.object.check_id = self.request.user
        self.object.product_id = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


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

class WishlistView(TemplateView):
    template_name = "wishlist.html"

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        product_detail = Product.objects.all()
        productList = Wishlist.objects.filter(current_user = self.request.user.myprofile)
    
        context["mywish_list"] = productList
        context['product_detail'] = product_detail
        return context

@login_required
def add_to_wishlist(req, pk):
    product = Product.objects.get(prid=pk)
    #print("Product list", product)
    Wishlist.objects.create(product = product, current_user = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/")

@login_required
def remove_from_wishlist(req, pk):
    product = Product.objects.get(prid=pk)
    Wishlist.objects.filter(product = product, current_user = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/")

def remove_from_table_wishlist(req, pk):
    product = Product.objects.get(prid=pk)
    Wishlist.objects.filter(product = product, current_user = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/wishlist")

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'pranav101sharma@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})









# @login_required()
# def wishlist(request, pk):
#     add_to_wishlist(request,pk)
#     product = Wishlist.objects.filter(product = pk)
#     product_details = Product.objects.filter()
#     return render(request, 'wishlist.html', {'product': product})






