from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import F

from .models import *


class Home(ListView):
	model = Post
	context_object_name = "posts"
	template_name = 'blog/index.html'
	paginate_by = 4
	
	def get_context_data(self, *, object_list=None, **kwargs):
		ctx = super(Home, self).get_context_data(**kwargs)
		ctx['title'] = 'Classic Blog Design'
		return ctx


class PostsByCategory(ListView):
	context_object_name = "posts"
	template_name = 'blog/index.html'
	paginate_by = 4
	allow_empty = False
	
	def get_context_data(self, *, object_list=None, **kwargs):
		ctx = super(PostsByCategory, self).get_context_data(**kwargs)
		ctx['title'] = Category.objects.get(slug=self.kwargs['slug'])
		return ctx
	
	def get_queryset(self):
		return Post.objects.filter(category__slug=self.kwargs['slug'])


class PostsByTag(ListView):
	context_object_name = "posts"
	template_name = 'blog/index.html'
	paginate_by = 4
	allow_empty = False
	
	def get_context_data(self, *, object_list=None, **kwargs):
		ctx = super(PostsByTag, self).get_context_data(**kwargs)
		ctx['title'] = 'Записи по тегу \'' + Tag.objects.get(slug=self.kwargs['slug']).title + '\''
		return ctx
	
	def get_queryset(self):
		return Post.objects.filter(tags__slug=self.kwargs['slug'])


class GetPost(DetailView):
	model = Post
	template_name = 'blog/single.html'
	context_object_name = "post"
	
	def get_context_data(self, *, object_list=None, **kwargs):
		ctx = super(GetPost, self).get_context_data(**kwargs)
		self.object.views = F('views') + 1
		self.object.save()
		self.object.refresh_from_db()
		return ctx


class Search(ListView):
	template_name = 'blog/search.html'
	context_object_name = "posts"
	paginate_by = 4

	def get_queryset(self):
		return Post.objects.filter(title__icontains=self.request.GET.get('s'))
	
	def get_context_data(self, *, object_list=None, **kwargs):
		ctx = super(Search, self).get_context_data(**kwargs)
		ctx['s'] = f"s={self.request.GET.get('s')}&"
		return ctx
	