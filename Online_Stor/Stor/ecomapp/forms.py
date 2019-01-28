# -*- coding: utf-8 -*-



from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

class LoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с данным логином не зарегистрирован в системе!')
		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise forms.ValidationError('Неверный пароль!')
			
	
		


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [ 									 #указываем поля 
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email'
		]
		
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['password'].help_text = 'Придумайте пароль'
		self.fields['password_check'].label = 'Повторите пароль'
		self.fields['password_check'].help_text = 'Повторите пароль'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label ='Фамилия'
		self.fields['email'].label = 'Ваша почта'
		self.fields['email'].help_text = 'Пожалуйста, указывайте реальный адрес'

	def clean(self):																	#создаем проверку 
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован в системе!')
		if password != password_check:
			raise forms.ValidationError('Ваши пароли не совпадают! Попробуйте снова!')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Пользователь с данной почтой уже зарегистрирован в системе!')

class OrderForm(forms.Form):
	first_name = forms.CharField(max_length=150)
	surname  = forms.CharField(max_length=150)
	phone = forms.CharField(max_length=12)
	buying_type = forms.ChoiceField(widget=forms.Select(), choices=(('self','Самовывоз' ),('delivery','Доставка'))) # widget=froms.Select()-выпадающее меню; choices=(('...','...'),('...'),('...'))-выбор выпадающего меню!
	date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
	user_email = forms.EmailField(max_length=200)
	address = forms.CharField(required=False)
	comments = forms.CharField(widget=forms.Textarea, required=False)

	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].label = 'Имя '
		self.fields['surname'].label = 'Фамилия '
		self.fields['phone'].label = ' Телефон '
		self.fields['phone'].help_text = ' Пожалуйста укажите свой номер телефона '
		self.fields['buying_type'].label = ' Способ получения  '
		self.fields['address'].label = ' Адрес доставки '
		self.fields['address'].help_text = ' Укажите свой Адрес: Страна/Регион-Край/Область/Регион-Город-Улица, дом, квартира '
		self.fields['user_email'].label = ' почта "email" '
		self.fields['user_email'].help_text = ' Укажите Вашу почту  '
		self.fields['comments'].label = 'Комментарии'
		self.fields['date'].label = ' Дата доставки '
		self.fields['date'].help_text = ' Доставка производится на следущий день после оформления заказа. Менеджер с Вами предварительно свяжется! '



		#скачать ещё нужно для html шаблона библиотеку django 'django-crispy-forms'!!!
		#после этого в файле settings.py  в самом незу прописать CRISPY_TEMPLATE_PACK = ' bootstrap3' 
		#и заинсталировать в crispy_forms В settings.py В разделе INSTALL_APP
	