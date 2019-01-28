from django.db import models
from django.utils.translation import to_locale, get_language, ugettext_lazy as _ # для импорта файла в другой модуль 
import uuid
from slugify import slugify
from baysmodels.models import OrderingBaseModel, BaseModel


class FiltersCategory(OrderingBaseModel):
	category = models.ForeignKey('ecomapp.Category', on_delete = models.CASCADE, related_name = 'filterscategory', verbose_name = ('Category'))
	slug = models.CharField(_("Slug"), default = "", max_length = 250)
	name = models.CharField(_("Name"), default = "", max_length = 250)

	def __str__(self):
		return self.name

	def save(self):
		if not self.slug:
			self.slug = slugify(self.name)

		super(FiltersCategory, self).sve()

	class Meta:
		verbose_name = ('Фильтер Категории')
		verbose_name_plural = ('Фильры Категорий')



# Create your models here.
