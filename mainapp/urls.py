from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('password_reset', password_reset_request, name='password_reset'),
    path('categories', categories, name='categories'),
    path('category/<str:id>/<slug:slug>', category, name='category'),
    path('products', products, name='products'),
    path('details/<str:id>/<slug:slug>', product_details, name='details'),
    path('signout', signout, name='signout'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('profile_update', profile_update, name='profile_update'),
    path('profile_password', profile_password, name='profile_password'),
    path('itemtocart', itemtocart, name='itemtocart'),
    path('cart', cart, name='cart'),
    path('deleteitem', deleteitem, name='deleteitem'),
    path('deleteall', deleteall, name='deleteall'),
    path('increase', increase, name='increase'),
    path('decrease', decrease, name='decrease'),
    path('checkout', checkout, name='checkout'),
    path('pay', pay, name='pay'),
    path('callback', callback, name='callback'),
]
