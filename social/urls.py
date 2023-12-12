from django.urls import path
from .viewsets import ProfileViewSet
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    #path("profile_list/", views.profile_list, name="profile_list"), #normal profile-list
    path("profile/<int:pk>", views.profile, name="profile"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_view, name="register"),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("twitter_like/<int:pk>", views.twitter_like, name="twitter_like"),
    path("unfollow/<int:pk>", views.unfollow, name="unfollow"),
    path("follow/<int:pk>", views.follow, name="follow"),
    path("delete_message/<int:pk>", views.delete_message, name="delete_message"),
    path("profiless/", views.profiless_list, name="profiless_list"),#just to practice serializer and viewset
    path("api/profiless/", ProfileViewSet.as_view({"get": "list"}), name="profiless-list"),#just to practice serializer and viewset
    path("message_show/<int:pk>", views.message_show, name="message_show"),
]
