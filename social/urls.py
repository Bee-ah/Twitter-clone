#import debug_toolbar
from django.contrib import admin
from django.urls import path , include
#importante quando for mudar para viewstes
from . import views 
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", views.home , name="home"),
    path("profile_list/" , views.profile_list , name="profile_list"),
    path("profile/<int:pk>" , views.profile , name="profile"),
    path("login/" , views.login_user , name="login"),
    path("logout/" , views.logout_user , name="logout"),
    path('register/', views.register_view, name='register'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('twitter_like/<int:pk>',views.twitter_like , name="twitter_like"),
    #path('login_or_register/<str:action>/', views.handle_login_or_register, name='handle_login_or_register'),
]
