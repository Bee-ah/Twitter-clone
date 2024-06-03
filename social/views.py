import io
from urllib.parse import urlparse
from django.http import HttpResponse, JsonResponse , FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from django.core.paginator import Paginator
from social.serializers.social_serializer import RegisterSerializer
from .models import Profile, Message
from .forms import MessageForm, ProfileEdit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont




#gets the domain of the link edit user
def get_domain_from_url(url):
    parsed_url = urlparse(url).netloc
    return parsed_url

#render the list of profile page
def profiless_list(request):
    if request.htmx:
        return render(request, "profiless_content.html")
    else:
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
        mensagens_list = Message.objects.all().order_by("-created_at")
        paginator = Paginator(mensagens_list, 10)
        page_number = request.GET.get('page') or 1
        mensagens = paginator.get_page(page_number)

        if request.htmx:
            return render(request, "messages.html", {"mensagens": mensagens.object_list,"page_obj":mensagens, "form": form})
        else:
            return render(request, "home.html", {"mensagens": mensagens.object_list,"page_obj":mensagens, "form": form})
        
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
        if request.htmx:
            return render(
            request,
            "profile_content.html",
            {
                "profile": profile,
                "mensagens": mensagens,
                "form": form,
                "followers": followers,
                "domain": domain,
            },
        )
        else:
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
            return JsonResponse({'success': True, 'redirect_url': reverse('home')})
        else:
            error_message = "Invalid login credentials. Please try again."
            return JsonResponse({'success': False, 'error_message': error_message})
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
            is_liked = False
        else:
            mensagem.likes.add(request.user)
            is_liked = True
        return JsonResponse({'is_liked': is_liked , 'like_count':mensagem.likes.count()})

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

#para gerar pdf
def generate_pdf(request , pk):
    if request.user.is_authenticated:
        user = User.objects.get(pk=pk)
        comments = Message.objects.filter(user_id=pk).order_by("-created_at")
        response = HttpResponse(content_type='data/pdf')
        response['Content-Disposition'] = f'attachment; filename="{user.username}_comments.pdf"'
         # Cria o PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
       
        width, height = letter
        font_path = 'static/fonts/Symbola.otf'
        pdfmetrics.registerFont(TTFont('Symbola', font_path))

         
        p.setStrokeColorRGB(0, 0, 1)  

      
        p.rect(5, 5, width-10, height-10, stroke=True, fill=False)

        # Define a fonte padrão para o título
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, height - 50, f"Messages from {user.username}")

        # Espaçamento inicial
        y = height - 80

        # Define a fonte para os comentários, incluindo emojis
        p.setFont("Symbola", 12)
        for comment in comments:
            if y < 50:  # Verifica se há espaço suficiente na página atual
                p.showPage()
                y = height - 50
                p.setFont("Symbola", 12)

            p.drawString(100, y, f"{comment.created_at:%Y-%m-%d %H:%M}: {comment.body}")
            y -= 20  # Espaçamento entre os comentários
        
        p.setFont("Helvetica", 10)
        p.drawString(100, 30, "© Twitter-Clone LTDA 2024")  

        p.showPage()
        p.save()
         
        pdf_data = buffer.getvalue()
        buffer.close()

        response.write(pdf_data)
        return response