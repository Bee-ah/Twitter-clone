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
]
