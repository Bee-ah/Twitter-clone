from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Profile , Message
from .forms import MessageForm

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
        return render(request , 'profile.html' , {"profile":profile , "mensagens":mensagens , "form": form})  
    else:
        messages.success(request , ("You must be logged in to view this page"))
        return redirect('home') 