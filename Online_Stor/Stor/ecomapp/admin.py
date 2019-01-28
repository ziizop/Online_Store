from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from ecomapp.models import Category, Brand, Product, CartItem, Cart, Order #ProductManager #Sklady


#class SkladyAdmin(admin.ModelAdmin):
	#list_display = ['address', 'phone']
#admin.site.register(Sklady, SkladyAdmin)


class ProductAdminInline(admin.TabularInline):
	model = Product
	extra = 0 
	

	
class AdminCategory(ModelAdmin):
    search_fields = ['name']        # поисковая строка по имени 
    list_display = ['name', 'slug'] # отображения в таблице графф  название и ссылка
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)} # функция автозаполнения slug по граффе название 
    inlines = [ProductAdminInline]
    


class ProductAdmin(admin.ModelAdmin):
	list_display = ['title','category', 'slug', 'price', 'available', 'created_at', 'updated_at']
	prepopulated_fields = {'slug':('title',)}
	search_fields = ['title']
	list_filter = ('title', 'category',)



class AdminOrder(ModelAdmin):
	search_fields = ['user', 'first_name', 'surname']
	list_display = ['status', 'buying_type', 'total', 'order_date','user', 'phone']
	list_filter = ['status', 'buying_type', ]


class AdminCart(ModelAdmin):
	list_display = ['id','catr_total',]


	
		
admin.site.register(Category, AdminCategory)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart, AdminCart)


#class OrderAdmin(admin.ModelAdmin):
	#list_display = ['user'
					#'first_name'
					#'surname'
					#'status'
					#'total'
					#'buying_type'
					#'order_date'
					#]
admin.site.register(Order,AdminOrder )

	

# Register your models here.
