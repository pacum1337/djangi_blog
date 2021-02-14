from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *


class PostAdminForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorUploadingWidget())
	
	class Meta:
		model = Post
		fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "category", "created_at", "author", "views", 'get_photo')
	prepopulated_fields = {'slug': ('title',)}
	form = PostAdminForm
	save_on_top = True
	search_fields = ("title", )
	list_filter = ("category", "author")
	readonly_fields = ('views', "created_at", "get_photo")
	fields = ("title", "slug", 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at')
	
	# save_as = True
	def get_photo(self, obj):
		if obj.photo:
			return mark_safe(f"<img src='{obj.photo.url}' width=50>")
		return "-"
	get_photo.short_description = "Фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("title",)
	prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("title",)
	prepopulated_fields = {'slug': ('title',)}
