#import debug_toolbar
from django.contrib import admin
from django.urls import path , include , re_path
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('social.urls')),
]
