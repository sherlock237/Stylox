from app.models import Product, Wishlist, MyProfile
from django import template

register = template.Library()

@register.simple_tag
def add_variable_to_context(request):  
    obList = Wishlist.objects.filter(current_user = request.user.myprofile)
    obno = obList.count()
    return obno

@register.filter
def get_int(value):
    return int(value)
            

        

