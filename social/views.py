from django import views
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from social.serializers.social_serializer import RegisterSerializer
from .models import Profile , Message
from .forms import MessageForm , ProfileEdit
#novo

def register_view(request):   
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        serializer = RegisterSerializer(data={'username': username, 'password': password})
        if serializer.is_valid():
            user = serializer.save()
#            user = authenticate(username = username , password = password)
            login(request, user)
            return redirect('home')
        else:
            error_messages = "Invalid registration data. Please try again."
            return render(request, 'login.html', {'error_messages': error_messages})
    else:
        return render(request , "login.html" , {})
        

def home(request):
    if request.user.is_authenticated:
        form = MessageForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                mensagem = form.save(commit=False)
                mensagem.user = request.user
                mensagem.save()
                messages.success(request , ("Your message was sent"))
                return redirect('home')
        mensagens = Message.objects.all().order_by("-created_at")
        return render(request , 'home.html' , {"mensagens": mensagens , "form":form})
    else:
        mensagens = Message.objects.all().order_by("-created_at")
        return render(request , 'home.html' , {"mensagens": mensagens})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request , 'profile_list.html' , {"profiles": profiles})
    else:
        messages.success(request , ("You must be logged in to view this page"))
        return redirect('home')

def profile(request , pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk) 
        followers = profile.follows.all()
        mensagens = Message.objects.filter(user_id = pk).order_by("-created_at") 
        form = MessageForm(request.POST or None)
        if request.method == "POST":
            if "follow" in request.POST:
                current_user_profile = request.user.profile
                action = request.POST['follow']
                if action =="unfollow":
                    current_user_profile.follows.remove(profile)
                elif action =="follow":
                    current_user_profile.follows.add(profile)
                current_user_profile.save()
            elif "form" in request.POST:
                if form.is_valid():
                    mensagem = form.save(commit=False)
                    mensagem.user = request.user
                    mensagem.save()
                    messages.success(request , ("Your message was sent"))
                    return redirect('profile' , pk=pk)
        return render(request , 'profile.html' , {"profile":profile , "mensagens":mensagens , "form": form , "followers": followers})  
    else:
        messages.success(request , ("You must be logged in to view this page"))
        return redirect('home') 
    
def login_user(request):
    error_message =None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password) 
        if user is not None:
            login(request,user) 
            messages.success(request , ("You have been logged in"))
            return redirect('home')
        else:
            error_message = "Invalid login credentials. Please try again."
        return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request , "login.html" , {})

def logout_user(request):
    logout(request)    
    messages.success(request , ("See you next time!"))
    return redirect('login')

def edit_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        profile_form = ProfileEdit(request.POST or None, request.FILES or None, instance=profile_user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, ("Your Profile Has Been Updated!"))
            return redirect('home')
        return render(request, "edit_user.html", {'profile_form':profile_form})
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')

def twitter_like(request , pk):
    if request.user.is_authenticated:
        mensagem = get_object_or_404(Message, id=pk)
        if mensagem.likes.filter(id=request.user.id):
            mensagem.likes.remove(request.user)
        else:
            mensagem.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))