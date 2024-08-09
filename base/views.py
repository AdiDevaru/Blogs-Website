from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import Blog, Review
from .forms import ReviewForm

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django import forms

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login

#User Authentication

class UserLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blogs')

class RegisterUser(FormView):
    form_class = UserCreationForm
    template_name = 'base/register.html'
    success_url = reverse_lazy('blogs')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blogs')
        return super(RegisterUser, self).get(*args, **kwargs)

#Blog CRUD
class BlogList(ListView):
    model = Blog
    template_name = 'base/blogs.html'
    context_object_name = 'blogs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search_item') or ''
        if search:
            context['blogs'] = context['blogs'].filter(title__startswith=search)
        context['search'] = search
        
        return context
    
class BlogDetails(DetailView):
    model = Blog
    template_name = 'base/blog.html'
    context_object_name = 'blog'
        
class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'base/createblog.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('blogs')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'description']
    template_name = 'base/createblog.html'
    success_url = reverse_lazy('blogs')
    
    
class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'base/deleteconfirm.html'
    success_url = reverse_lazy('blogs')
    
#Reviews
class ReviewCreate(LoginRequiredMixin, CreateView):
    
    model = Review
    template_name = 'base/createreview.html'
    form_class = ReviewForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)
    
    
    success_url = reverse_lazy('blogs')   

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['body', 'vote']
    template_name = 'base/createreview.html'
    success_url = reverse_lazy('blogs')
    
class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'base/deleteconfirmreview.html'
    success_url = reverse_lazy('blogs')