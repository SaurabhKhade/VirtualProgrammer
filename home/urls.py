from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('signup/',views.HandleSignup,name='signup'),
    path('logout/',views.HandleLogout,name='logout'),
    path('login/',views.HandleLogin,name='login'),
    path('like/',views.like,name='like'),
]
