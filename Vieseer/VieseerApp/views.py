from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from VieseerApp.forms import RegisterForm,ImageUploadForm
from VieseerApp.models import Image
# Create your views here.

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user) 
            return redirect('gallery')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gallery')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('gallery')

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.author = request.user
            new_image.save()
            return redirect('gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def gallery(request):
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery.html', {'images': images})