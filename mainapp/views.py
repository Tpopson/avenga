import uuid
import requests
import json 


from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from mainapp.models import Category,Product
from account.models import Profile
from cart.models import *
from account.forms import SignupForm, ProfileForm, PasswordForm
# Create your views here.


def index(request):
    categorys = Category.objects.all().order_by('-id')[:4]

    context = {
        'categorys':categorys
    }
    return render(request, 'index.html', context)


def products(request):
    products = Product.objects.all()
   
    context = {
        'products':products,
    }
    return render(request, 'products.html', context)


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }
    return render(request, 'categories.html', context)


def category(request, id, slug):
    single_category = Product.objects.filter(category_id=id)
                          
    context = {
        'single_category':single_category
    }
    return render(request, 'category.html', context)


def product_details(request, id, slug):
    details = Product.objects.get(pk=id)

    context = {
        'details':details
    }
    return render(request, 'details.html', context)


#authentication system
def signout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('signin')


def signin(request):
    if request.method =="POST":
        name = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username = name, password = passw)
        if user:
            login(request, user)
            messages.success(request, 'Signin successful!')
            return redirect('index')
        else:
            messages.warning(request, 'Username/password incorrect')
            return redirect('signin')
    return render(request, 'signin.html')


def signup(request):
    regform = SignupForm()#instantiate the signup form for  a GET request
    if request.method == 'POST':
        phone = request.POST['phone']
        regform = SignupForm(request.POST)#instantiate the signup form for a POST request
        if regform.is_valid():
            newuser = regform.save()
            newprofile = Profile(user = newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.save()
            login(request, newuser)
            messages.success(request, 'Signup successful!')
            return redirect('index')
        else:
            messages.error(request, regform.errors)
    return render(request, 'signup.html')

#authentication system done 


# user profile 
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile':profile
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    # profile update 
    update = ProfileForm(instance=request.user.profile)#instatiate the profile update form for a GET request
    if request.method == 'POST':
        update = ProfileForm(request.POST, request.FILES,  instance=request.user.profile)#instatiate the profile update form for a POST request
        if update.is_valid():
            update.save()
            messages.success(request, 'Profile Update successful!')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profile_update')

    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html', context)


@login_required(login_url='signin')
def profile_password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordForm(request.user)
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password change is successful.')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('profile_password')

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profile_password.html', context)
# user profile done

# shopcart 
@login_required(login_url='signin')
def itemtocart(request):
    order_no = Profile.objects.get(user__username = request.user.username)
    buyer_id = order_no.id
    if request.method == 'POST':
        itemquantity = int(request.POST['quantity'])
        itemid = request.POST['productid']
        selecteditem = Product.objects.get(pk=itemid)
        basket = Shopcart.objects.filter(user__username = request.user.username, paid= False)
        if basket:
            cart = Shopcart.objects.filter(product= selecteditem, user__username = request.user.username ,paid=False).first()
            if cart:
                cart.quantity += itemquantity
                cart.amount = cart.quantity * cart.price
                cart.save()
                messages.success(request, 'Your order is being processed.')
                return redirect('products')
            else:
                newitem = Shopcart()
                newitem.user = request.user
                newitem.product = selecteditem
                newitem.price = selecteditem.p_price
                newitem.quantity = itemquantity
                newitem.amount = itemquantity * selecteditem.p_price
                newitem.cart_no = buyer_id
                newitem.save()
                messages.success(request, 'Your order is being processed.')
                return redirect('products')
        else:
            newcart = Shopcart()
            newcart.user = request.user
            newcart.product = selecteditem
            newcart.price = selecteditem.p_price
            newcart.quantity = itemquantity
            newcart.amount = itemquantity * selecteditem.p_price
            newcart.cart_no = buyer_id
            newcart.save()
            messages.success(request, 'Your order is being processed.')
    return redirect('products')



@login_required(login_url='signin')
def cart(request):
    cartitems = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    for a in cartitems:
        subtotal += a.amount

    vat = 0.075 * subtotal 

    total = vat + subtotal 

    context = {
        'cartitems':cartitems,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    return render(request, 'cart.html', context)



@login_required(login_url='signin')
def deleteitem(request):
    if request.method == 'POST':
        itemid = request.POST['itemid']
        deletecartitem = Shopcart.objects.get(pk = itemid)
        deletecartitem.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('cart')


@login_required(login_url='signin')
def deleteall(request):
    if request.method == 'POST':
        deletecart = Shopcart.objects.filter(user__username = request.user.username, paid = False)
        deletecart.delete()
        messages.success(request, 'All cart items deleted successfully!')
    return redirect('cart')


@login_required(login_url='signin')
def increase(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        item_id = request.POST['itemid']
        newquantity = Shopcart.objects.get(pk=item_id)
        newquantity.quantity += quantity
        newquantity.amount = newquantity.quantity * newquantity.price
        newquantity.save()
        messages.success(request, 'Quantity updated!')
    return redirect('cart')


@login_required(login_url='signin')
def decrease(request):
    if request.method == 'POST':
        item_id = request.POST['itemid']
        newquantity = Shopcart.objects.get(pk=item_id)
        newquantity.quantity -= int(1)
        newquantity.amount = newquantity.quantity * newquantity.price
        newquantity.save()
    return redirect('cart')




@login_required(login_url='signin')
def checkout(request):
    cartitems = Shopcart.objects.filter(user__username = request.user.username, paid=False)
    profile = Profile.objects.get(user__username = request.user.username)
    subtotal = 0
    for a in cartitems:
        subtotal += a.amount

    vat = 0.075 * subtotal 

    total = vat + subtotal 

    context = {
        'cartitems':cartitems,
        'total':total,
        'profile':profile,
    }
    return render(request, 'checkout.html', context)

    
    

@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://34.240.124.29/callback'
        # cburl = 'http://localhost:8000/callback'
        ref = str(uuid.uuid4())
        amount = float(request.POST['total']) * 100
        cartno = request.POST['cartno']
        email = request.user.email
        user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        order_address = request.POST['order_address']
        delivery_address = request.POST['delivery_address']
        city = request.POST['city']
        state = request.POST['state']

        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'amount': int(amount), 'email': email, 'order_number': cartno, 'callback_url': cburl}

        try:
            r = requests.post(curl, headers=headers, json= data)
        except Exception:
            messages.error(request, 'Network busy')
        else:   
            transback = json.loads(r.text)
            rurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.total = amount
            account.cart_no = cartno
            account.pay_code = ref
            account.status = 'New'
            account.paid = True
            account.save()


            delivery = Shipping()
            delivery.user = user
            delivery.first_name = first_name
            delivery.last_name = last_name
            delivery.email = email
            delivery.phone = phone
            delivery.billing_address = order_address
            delivery.delivery_address = delivery_address
            delivery.city = city
            delivery.state = state
            delivery.save()
            
            return redirect(rurl)
    return redirect('checkout')




def callback(request):
    profile = Profile.objects.get(user__username = request.user.username)
    cart = Shopcart.objects.filter(user__username = request.user.username, paid= False)

    for item in cart:
        item.paid = True
        item.save()

        stock = Product.objects.get(pk= item.product.id)
        stock.p_max -= item.quantity 
        stock.save()

    context = {
        'profile':profile
    }
    return render(request, 'callback.html', context)
# shopcart done