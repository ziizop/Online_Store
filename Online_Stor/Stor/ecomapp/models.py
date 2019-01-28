from django.db import models 
from django.conf import settings
from django.db.models.signals import pre_save #для авто заполнения
from django.utils.text import slugify #берет поля и превращает в поле с типом slug
from django.urls import reverse  #для создания ссылок на объекты 
from transliterate import translit # библиотека для перевода с керилицы в латиницу .Установить через pip (pip install transliterate)
from mptt.models import MPTTModel, TreeForeignKey  # создает дерево 

# Create your models here.

#class Sklady(models.Model):
	#address = models.CharField(max_length=150, verbose_name="Адрес")
	#phone  = models.CharField(max_length=12, verbose_name="Телефон")
	 		



class Category (models.Model):
	name = models.CharField(max_length=150, verbose_name='Название')
	slug = models.SlugField(max_length=150, unique=True ,blank=True, verbose_name='Ссылка',)


	def __str__(self):
		return self.name

	def get_absoulute_url(self):
		return  reverse('category_detail', kwargs={'category_slug': self.slug})

	class Meta:
		verbose_name = ('Категория')
		verbose_name_plural = ('Категории')
			



def pre_save_category_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(translit(unicode(instance.name), reversed=True))
		instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)





	



class Brand(models.Model):
	name = models.CharField(max_length=150, verbose_name='Название')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = ('Бренд')
		verbose_name_plural = ('Бренды')


def image_folder(instance, filename):                       
		filename = instance.slug + '.' + filename.split('.')[1] #переопределяем название файла которого скачали ( filename ) который разделяет наш файл на название и его расширение 
		return "{0}/{1}".format(instance.slug, filename)  # возвращаем строку идет подсановка методом format и записываем эту функцию в upload_to

#class ProductManager(models.Model):

	 # #def all(self, *args, **kwargs):
	  	#return super(ProductManager, self).get_queryset().filter(available=True) # для того чтобы на сайте не отображался товар которого нет в наличии 
	
		

class Product(models.Model):
	category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.CASCADE)
	brand = models.ForeignKey(Brand, verbose_name='брэнд', on_delete=models.CASCADE)
	#sklady = models.ManyToManyField(Sklady, verbose_name= 'Склады')
	title = models.CharField(max_length=150, verbose_name='Название',  )
	slug  = models.SlugField(max_length=150, verbose_name='Ссылка', blank=True)
	description = models.TextField(blank=True, verbose_name='Описание')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to=image_folder, default=True)
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
	available = models.BooleanField(default=True, verbose_name='В наличии/не в наличии')
	#objects = ProductManager()

	def __str__(self):
		return self.title

	def get_absoulute_url(self):
		return  reverse('product_detail', kwargs={'product_slug': self.slug})

	class Meta:
		verbose_name = ('Продук')
		verbose_name_plural = ('Продукты')



def pre_save_product_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(translit(unicode(instance.name), reversed=True))
		instance.slug = slug
pre_save.connect(pre_save_product_slug, sender=Product)


	



class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукты')
	qty = models.PositiveIntegerField(default=1, verbose_name='количество')
	item_total =models.DecimalField(max_digits=9, decimal_places=2, default=0.00)


	def __str__(self):
		return "Cart item for product {0}".format(self.product.title)

	class Meta:
		verbose_name = ('Элемент Корзины')
		verbose_name_plural = ('Элементы Корзин')



class Cart(models.Model):
	items = models.ManyToManyField(CartItem, blank=True)
	catr_total = models.DecimalField(max_digits=9 , decimal_places=2 , default=0.00)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = ('Корзина')
		verbose_name_plural = ('Корзины')



	def add_to_cart(self, product_slug):
		cart = self
		product = Product.objects.get(slug=product_slug)
		new_item, _= CartItem.objects.get_or_create(product = product, item_total=product.price)  
		if new_item not in cart.items.all():
			cart.items.add(new_item)
			cart.save()

	def remove_from_cart(self, product_slug):
		cart = self
		product = Product.objects.get(slug=product_slug)
		for cart_item in cart.items.all():
			if cart_item.product == product:
				cart.items.remove(cart_item)
				cart.save()



	def change_qty(self, qty, item_id):
		cart = self
		cart_item = CartItem.objects.get(id=int(item_id))
		cart_item.qty = int(qty)
		cart_item.item_total = int(qty)* float(cart_item.product.price)
		cart_item.save()
		new_cart_total = 0.00
		for item in cart.items.all():
			new_cart_total += float(item.item_total)
		cart.catr_total = new_cart_total
		cart.save()


ORDER_STATUS_CHOICES = (
	('принят в обработку', 'принят в обработку' ),
	('Выполняется','Выполняется'),
	('Оплачен','Оплачен')
)

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0] , verbose_name='Статус заказа')
	items = models.ManyToManyField(Cart)
	buying_type = models.CharField(max_length=40, choices=(('Самовывоз','Самовывоз' ),('Доставка','Доставка')), default='Самовывоз', verbose_name='тип заказа')
	total = models.DecimalField(max_digits=9 , decimal_places=2 , default=0.00, verbose_name='Общая сумма')
	order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
	first_name = models.CharField(max_length=150, verbose_name='Имя')
	surname  = models.CharField(max_length=150, verbose_name='Фамилия')
	phone = models.CharField(max_length=12, verbose_name='Телефон')
	user_email = models.EmailField(max_length=200, verbose_name='почта пользователя ')
	address = models.CharField(max_length=600, verbose_name='Адрес')
	comments = models.TextField(verbose_name='комментарии')

	def __str__(self):
		return "Заказ №{0}".format(str(self.id))

	class Meta:
		verbose_name = ('Заказ')
		verbose_name_plural = ('Заказы')





		

			
	
		




	


	




