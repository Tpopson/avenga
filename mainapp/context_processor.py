from .models import Category
from cart.models import Shopcart


def catedropdown(request):
    categories = Category.objects.all()

    context ={
        'categories':categories
    }

    return context 


def itemcount(request):
    item_count = Shopcart.objects.filter(user__username= request.user.username, paid=False)

    cart_counter = 0
    for item in item_count:
        cart_counter += item.item_carted

    context ={
        'cart_counter':cart_counter
    }

    return context