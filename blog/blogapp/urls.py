
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogHome, name="bloghome"),
    path('<int:id>', views.blogPost, name="blogPost"),
    path('dashboard', views.dashboard, name="dash"),
    path('addpost', views.add, name="add"),
    path('updatepost/<int:id>', views.update, name="update"),
    path('deletepost/<int:id>', views.delete, name="delete"),
    path('postComment', views.postComment, name="postComment"),
    ]