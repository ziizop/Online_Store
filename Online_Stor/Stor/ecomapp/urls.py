from django.conf.urls import url, include
from ecomapp.views import ( 
				base_view, 
				category_view, 
				product_view, 
				cart_view, 
				add_to_cart_view, 
				remove_from_cart_view, 
				change_items_qty, 
				checkout_view, 
				order_create_view, 
				make_order_view, 
				account_view,
				registration_view,
				login_view,
				logout_view
							)
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', base_view, name='base'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
	url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
	url(r'^add_to_cart/$', add_to_cart_view, name='add_to_cart'), # добовляет товар в корзину 
	url(r'^remove_from_cart/$', remove_from_cart_view, name='remove_from_cart'), # удаляет товар из корзины
	url(r'^change_items_qty/$', change_items_qty, name='change_items_qty'),#добовления кол-ва товара 
	url(r'^checkout/$', checkout_view, name='checkout'),
	url(r'^order_create/$', order_create_view, name='order_create'),
	url(r'^make_order/$', make_order_view, name='make_order'),
	url(r'^thank_you/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
	url(r'^account/$', account_view, name='account'),
	url(r'^logout/$',logout_view, name='logout'),
	url(r'^login/$', login_view, name='login'),
	url(r'^registration/$', registration_view, name='registration'),
    url(r'^cart/$', cart_view, name='cart'),
    ]