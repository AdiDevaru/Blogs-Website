from django.urls import path
from . import views
from .views import BlogList, BlogDetails, BlogCreate, BlogUpdate, BlogDelete, ReviewCreate, ReviewUpdate, ReviewDelete, UserLogin, RegisterUser
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='blogs'), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('', BlogList.as_view(), name='blogs'),
    path('blog/<int:pk>/', BlogDetails.as_view(), name='blog'),
    path('blog-create', BlogCreate.as_view(), name='addblog'),
    path('blog-update/<int:pk>/', BlogUpdate.as_view(), name='updateblog'),
    path('blog-delete/<int:pk>/', BlogDelete.as_view(), name='deleteblog'),
    path('blog/<int:pk>/review-create/', ReviewCreate.as_view(), name='addreview'),
    path('review-update/<int:pk>/', ReviewUpdate.as_view(), name='updatereview'),
    path('review-delete/<int:pk>/', ReviewDelete.as_view(), name='deletereview'),
]
