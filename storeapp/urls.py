from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('product/<str:slug>', views.detail, name = 'detail'),
    path('category/<str:slug>', views.category, name = 'category'),
    path('cart', views.cart, name = 'cart'),
    path('updatecart', views.updateCart, name = 'updatecart'),
    path('updatequantity', views.updateQuantity),
    path('deleteitems', views.deleteCartitems),
    path('checkout', views.checkout, name = 'checkout'),
    path('payment', views.confirmPayment),
    path('saveditems', views.saveItems, name = 'saveitems'),
    path('addsaveitems', views.addSavedItems),
    path('order', views.order, name = 'order'),
    path('account', views.account, name = 'account'),
    path('updateaccount', views.update_user_info, name = 'updateaccount'),
    path('search', views.search, name = 'search')


]