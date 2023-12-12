from urllib.parse import urlparse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from social.serializers.social_serializer import RegisterSerializer
from .models import Profile, Message
from .forms import MessageForm, ProfileEdit
from django.shortcuts import render

#gets the domain of the link edit user
def get_domain_from_url(url):
    parsed_url = urlparse(url).netloc
    return parsed_url

#render the list of profile page
def profiless_list(request):
    return render(request, "profiless.html")

#register user
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        serializer = RegisterSerializer(
            data={"username": username, "password": password}
        )
        if serializer.is_valid():
            user = serializer.save()
            # arruma bug de follow itself
            profile = Profile.objects.get(user=user)
            user.profile.follows.remove(profile)

            login(request, user)
            return redirect("home")
        else:
            error_messages = "Invalid registration data. Please try again."
            return render(request, "login.html", {"error_messages": error_messages})
    else:
        return render(request, "login.html", {})


def home(request):
    if request.user.is_authenticated:
        form = MessageForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                mensagem = form.save(commit=False)
                mensagem.user = request.user
                mensagem.save()
                messages.success(request, ("Your message was sent"))
                return redirect("home")
        mensagens = Message.objects.all().order_by("-created_at")
        return render(request, "home.html", {"mensagens": mensagens, "form": form})
    else:
        mensagens = Message.objects.all().order_by("-created_at")
        return render(request, "home.html", {"mensagens": mensagens})

#profile list without django rest framework
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")

#unfollow a user
def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        # unfollow user
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")

#follow a user
def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        # follow user
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")

#show profile
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        followers = profile.follows.all()
        domain = get_domain_from_url(profile.profile_website)
        mensagens = Message.objects.filter(user_id=pk).order_by("-created_at")
        form = MessageForm(request.POST or None)
        if request.method == "POST":
            if "follow" in request.POST:
                current_user_profile = request.user.profile
                action = request.POST["follow"]
                if action == "unfollow":
                    current_user_profile.follows.remove(profile)
                elif action == "follow":
                    current_user_profile.follows.add(profile)
                current_user_profile.save()
            elif "form" in request.POST:
                if form.is_valid():
                    mensagem = form.save(commit=False)
                    mensagem.user = request.user
                    mensagem.save()
                    messages.success(request, ("Your message was sent"))
                    return redirect("profile", pk=pk)
        return render(
            request,
            "profile.html",
            {
                "profile": profile,
                "mensagens": mensagens,
                "form": form,
                "followers": followers,
                "domain": domain,
            },
        )
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("home")

#login 
def login_user(request):
    error_message = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect("home")
        else:
            error_message = "Invalid login credentials. Please try again."
        return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html", {})

#logout
def logout_user(request):
    logout(request)
    return redirect("login")

#edit user profile: bio, location...
def edit_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        profile_form = ProfileEdit(
            request.POST or None, request.FILES or None, instance=profile_user
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, ("Your Profile Has Been Updated!"))
            return redirect("home")
        return render(request, "edit_user.html", {"profile_form": profile_form})
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect("home")

#give a like to a message
def twitter_like(request, pk):
    if request.user.is_authenticated:
        mensagem = get_object_or_404(Message, id=pk)
        if mensagem.likes.filter(id=request.user.id):
            mensagem.likes.remove(request.user)
        else:
            mensagem.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

#show message and reply
def message_show(request, pk):
    mensagem = get_object_or_404(Message, id=pk)
    if mensagem:
        reply_form = MessageForm(request.POST or None, parent_message=mensagem)
        if request.method == "POST":
            if reply_form.is_valid():
                new_message = reply_form.save(commit=False)
                new_message.user = request.user
                new_message.parent_message = mensagem
                new_message.save()
                messages.success(request, "Your reply was sent.")
                return redirect("message_show", pk=pk)
        return render(
            request,
            "message_show.html",
            {"mensagem": mensagem, "reply_form": reply_form},
        )
    else:
        messages.success(request, ("That message does not exist..."))
        return redirect("home")

#reply another message
def reply(request, parent_message_id=None):
    if request.user.is_authenticated:
        parent_message = None
        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)
        reply_form = MessageForm(request.POST or None, parent_message=parent_message)
        if request.method == "POST":
            if reply_form.is_valid():
                mensagem = reply_form.save(commit=False)
                mensagem.user = request.user
                mensagem.parent_message = parent_message
                mensagem.save()
                messages.success(request, ("Your message was sent"))
                return redirect("message_show", pk=parent_message_id)
        mensagens = Message.objects.all().order_by("-created_at")
        return render(
            request,
            "message_show.html",
            {
                "mensagens": mensagens,
                "reply_form": reply_form,
                "parent_message": parent_message,
            },
        )

#delete message
def delete_message(request, pk):
    if request.user.is_authenticated:
        mensagem = get_object_or_404(Message, id=pk)
        if request.user.username == mensagem.user.username:
            mensagem.delete()
            messages.success(request, ("The post has been deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("The post is not yours!"))
            return redirect("home")
    else:
        messages.success(request, ("Please log in to do this action"))
        return redirect(request.META.get("HTTP_REFERER"))
