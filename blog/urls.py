from django.urls import path
from . import views

urlpatterns = [
    path('',views.blogs,name='blogs'),
    path('search',views.search,name='search'),
    path('postComment',views.postComment,name='postComment'),
    path('<str:title>',views.site,name='blogsite'),
]
