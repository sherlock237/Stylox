from email import message
from django.views.generic.base import TemplateView
from app.models import Banner
from django.shortcuts import render, redirect
from .models import Banner,Product, Checkout, Wishlist, MyProfile,Subscribe, Contact,Cart
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
from django.core import serializers
from django.db.models import Count
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict
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




class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)  
        productList = Product.objects.all()   

        if not self.request.user.is_authenticated:
            for p11 in productList:  
            #print(p11)
                p11.wished = False
                p11.wishedno = 0

        else:
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
        length=0
        if not self.request.user.is_authenticated:
            print()
        else:
            p4=Cart.objects.filter(user_id=self.request.user)
            p4=serializers.serialize('json',list(p4))
            context['add_cart']=p4
            l=Cart.objects.filter(user_id=self.request.user)
            for i in l:
                length=length+i.quantity
            context['prd_len']=length


  
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
        if self.request.method =='POST' and self.request.POST['action']=='add_cart':
            listt=[]
            prd_id=self.request.POST.get('data')
            if(Cart.objects.filter(product_id=prd_id,user_id=self.request.user)):
                context={
                'add_prd':listt,
                    }
                return JsonResponse(context)
            else:
                product = Product.objects.get(prid=prd_id)
                prd_save=Cart(user_id=self.request.user,product_id=product,quantity=1,price=product.Current_price)
                prd_save.save()
            cart=Cart.objects.filter(product_id=prd_id,user_id=self.request.user)
            for i in cart:
                listt.append(i.product_id)
            listt=serializers.serialize('json',listt)
            l=Cart.objects.filter(user_id=self.request.user)
            length=0
            for i in l:
                length=length+i.quantity
            # print(length)            
            context={
                'add_prd':listt,
                'length':length,
            }
            return JsonResponse(context)

        
                
def loginpage(request):
    return render(request, "login.html") 

@login_required
def cart(request):
    if request.method =='POST' and request.POST['action']=='size_upd':
        prd_id=request.POST.get('pr_id')
        size=request.POST.get('size')
        if(Cart.objects.filter(product_id=prd_id,user_id=request.user)):
            size_upd=Cart.objects.get(product_id=prd_id,user_id=request.user)
            size_upd.size=size
            size_upd.save()
            context={
                'upd_size':size,
                    }
            return JsonResponse(context)

    if request.method =='POST' and request.POST['action']=='cart_qty':
        prd_id=request.POST.get('pr_id')
        qty=request.POST.get('qty')
        qty=int(qty)
        product = Product.objects.get(prid=prd_id)
        prd_save=Cart.objects.get(user_id=request.user,product_id=product)
        prd_save.quantity=qty
        prd_save.price=product.Current_price*qty
        prd_save.save()
        usr_cart=Cart.objects.filter(user_id=request.user)
        l=Cart.objects.filter(user_id=request.user)
        length=0
        for i in l:
            length=length+i.quantity
        context={
        'prd_len':length,
        'price':product.Current_price*qty,
            }
        return JsonResponse(context)
    if request.method =='POST' and request.POST['action']=='del':
        prd_id=request.POST.get('pr_id')
        product = Product.objects.get(prid=prd_id)
        prd_del=Cart.objects.get(user_id=request.user,product_id=product)
        prd_del.delete()
        usr_cart=Cart.objects.filter(user_id=request.user)
        l=Cart.objects.filter(user_id=request.user)
        length=0
        for i in l:
            length=length+i.quantity
        context={
        'prd_len':length,
            }
        return JsonResponse(context)
    usr_cart=Cart.objects.filter(user_id=request.user)
    l=Cart.objects.filter(user_id=request.user)
    length=0
    for i in l:
        length=length+i.quantity
    size_list=[]
    size_listt=[]
    final_size_list=[]
    for i in l:
        prd=Product.objects.filter(prid=i.product_id.prid)
        size_list.append(prd)
        
        final_size_list.append(i.size)
    size=0
    for i in size_list:
        for j in i:
            size=j.size_available
            size=size.split(',')
            size_listt.append(size)
    c=0
    for i in final_size_list:
        if(i is not ''):
            size_listt[c]=[i]+size_listt[c]
            size_listt[c]=list(OrderedDict.fromkeys(size_listt[c]))
        c+=1
        


    context={
        'usr_cart':zip(usr_cart,size_listt),
        'prd_len':length,
        
    }
        

    return render(request, "cart.html",context)
def contact(request):
    if request.method == 'POST':
        msg = request.POST.get("contactMessage")
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")

        contact = Contact(
            name = name,
            email = email,
            additional_information = msg,
            subject = subject
        )

        contact.save()
        stri = "Thank you for contacting us. We'll reach you soon."
        return render(request, 'contact.html', {'message': stri})


    return render(request, 'contact.html')

def register(request):
    return render(request, "register.html")

def singleproduct(request,prid): 
    if request.method =='POST' and request.POST['action']=='size_upd':
        prd_id=request.POST.get('pr_id')
        size=request.POST.get('size')
        if(Cart.objects.filter(product_id=prd_id,user_id=request.user)):
            size_upd=Cart.objects.get(product_id=prd_id,user_id=request.user)
            size_upd.size=size
            size_upd.save()
            context={
                'upd_size':size,
                    }
            return JsonResponse(context)


    if request.method =='POST' and request.POST['action']=='btn_add':
        prd_id=request.POST.get('pr_id')
        size=request.POST.get('size')
        if(Cart.objects.filter(product_id=prd_id,user_id=request.user)):
            print()
        else:
            product = Product.objects.get(prid=prd_id)
            prd_save=Cart(user_id=request.user,product_id=product,quantity=1,size=size,price=product.Current_price)
            prd_save.save()
            l=Cart.objects.filter(user_id=request.user)
            length=0
            for i in l:
                length=length+i.quantity
            context={
                'prd_len':length,
                    }
            return JsonResponse(context)



    prd=Product.objects.filter(prid=prid)
    size=0
    for i in prd:
        size=i.size_available
        break
    size=size.split(',')
    l=Cart.objects.filter(user_id=request.user)
    l=list(l)
    length=0
    for i in l:
        length=length+i.quantity
    prd_car=serializers.serialize('json',l)
    context={
        'prd':prd,
        'size':size,
         'prd_len':length,
         'prd_cart':prd_car,
    }
    return render(request, 'single-product.html',context)




# @method_decorator(login_required, name='dispatch')
# class checkoutview(CreateView):
#     template_name = 'checkout_form.html'
#     model = Checkout
#     fields = ['First_Name', 'Last_Name', 'company', 'address' , 'state', 'city', 'zip_code', 'email', 'phone' , 'Additional_information']

#     def form_valid(self, form):
#         self.object = form.save()
#         self.object.check_id = self.request.user
#         self.object.product_id = self.request.user
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())


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
        length=0
        l=Cart.objects.filter(user_id=self.request.user)
        l=list(l)
        prd_cart=[]
        for i in l:
            for j in productList:
                if(i.product_id.prid==j.product.prid):
                    prd_cart.append(i)
        for i in l:
            length=length+i.quantity
        context['prd_len']=length
        prd_cart=serializers.serialize('json',prd_cart)
        context['prd_cart']=prd_cart
        return context
    def post(self,*args, **kwargs):
        if self.request.method =='POST' and self.request.POST['action']=='btn_add':
            prd_id=self.request.POST.get('pr_id')
            if(Cart.objects.filter(product_id=prd_id,user_id=self.request.user)):
                print()
            else:
                product = Product.objects.get(prid=prd_id)
                prd_save=Cart(user_id=self.request.user,product_id=product,quantity=1,price=product.Current_price)
                prd_save.save()
            l=Cart.objects.filter(user_id=self.request.user)
            length=0
            for i in l:
                length=length+i.quantity
            context={
                'prd_len':length,
                    }
            return JsonResponse(context)




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
def emailit(receiver_email,content,ctype):
    #print(receiver_email)
    sender_email = ""
    password = ""
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Stylox Admin:Password Reset Requested "
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(content,ctype)
    message.attach(part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

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




@login_required
def checkout(request):
    model = Cart


    cart = Cart.objects.filter(user_id = request.user).values('product_id').annotate(total=Count('product_id')).order_by()
    product = Product.objects.all()

    total = 0

    for ci in cart:
        for p in product:
            if( p.prid == ci['product_id']):
                total += ci['total']*p.Current_price

    if request.method == 'POST':
        msg = request.POST.get("message")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        cname = request.POST.get("cname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip")
        phone = request.POST.get("phone")

        billing = Checkout(
            First_Name = fname,
            Last_Name = lname,
            company = cname,
            address = address,
            city = city,
            state = state,
            zip_code = zip,
            phone = phone, 
            email = email,
            Additional_information = msg
        )

        billing.save()

        message= "We've saved your billing address"

        return render(request, "checkout_form.html", {'mess': message, 'cart_list': cart, 'product': product, 'total': total})
    return render(request, "checkout_form.html", {'cart_list': cart, 'product': product,  'total': total})
    

def shop(request,pk):
    prd = Product.objects.filter(category=pk)
    li = len(prd)
    l=Cart.objects.filter(user_id=request.user)
    l=list(l)
    length=0
    for i in l:
        length=length+i.quantity
    context={'product':prd,'prd_len':length,'li':li}
    return render(request,"shop-grid-list-left-sidebar.html",context)

# @login_required()
# def wishlist(request, pk):
#     add_to_wishlist(request,pk)
#     product = Wishlist.objects.filter(product = pk)
#     product_details = Product.objects.filter()
#     return render(request, 'wishlist.html', {'product': product})






