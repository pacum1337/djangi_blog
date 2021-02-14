from django.db import models
from django.urls import reverse


class Category(models.Model):
	title = models.CharField("Название категории", max_length=255)
	slug = models.SlugField("URL категории", unique=True)
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "Категория(ю)"
		verbose_name_plural = "Категории"
		ordering = ['title']
	
	def get_absolute_url(self):
		return reverse("category", kwargs={"slug": self.slug})


class Tag(models.Model):
	title = models.CharField("Название тега", max_length=50)
	slug = models.SlugField("URL тега", unique=True)
	
	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse("tag", kwargs={"slug": self.slug})
	
	class Meta:
		ordering = ['title']
		verbose_name = "Тег"
		verbose_name_plural = "Теги"


class Post(models.Model):
	title = models.CharField("Название записи", max_length=255)
	author = models.CharField("Автор записи", max_length=150)
	content = models.TextField("Контент записи", blank=True)
	created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
	photo = models.ImageField("Фото публикации", upload_to='photos/%Y/%m/%d/', blank=True)
	slug = models.SlugField("URL записи", unique=True)
	views = models.PositiveIntegerField("Кол-во просмотров", default=0)
	category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT, related_name='posts')
	tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name='posts')
	
	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse("post", kwargs={"slug": self.slug})
	
	class Meta:
		ordering = ['-created_at']
		verbose_name = "Запись"
		verbose_name_plural = "Записи"
