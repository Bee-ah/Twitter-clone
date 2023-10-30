#import debug_toolbar
from django.contrib import admin
from django.urls import path , include
#importante quando for mudar para viewstes
from . import views 
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", views.home , name="home"),
]
