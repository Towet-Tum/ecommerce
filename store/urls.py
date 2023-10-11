from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="home"),
    path('product_deatil/<int:vehicle_id>/', views.product_detail, name='product_detail'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

     path('customer_registration_view/', views.customer_registration_view, name='signup'),
    path('customer_login_view/', views.customer_login_view, name='login'),
    path('customer_logout_view/', views.customer_logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('contact_success_view/', views.contact_success_view, name='contact_success'),
    path('login_success_view/', views.login_success_view, name="login_success"),
    path('lexus/', views.lexus, name='lexus'),
    path('bmw/', views.bmw, name='bmw'),
    path('mercedes/', views.mercedes, name='mercedes'),
    path('mazda/', views.mazda, name='mazda'),
    path('audi/', views.audi, name='audi'),
    path('product_search/', views.product_search, name='search_products'),

]