from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404,JsonResponse
import os
from django.core.files.storage import default_storage
from django.db.models import Prefetch
from VieseerApp.forms import RegisterForm,ImageUploadForm,CollectionForm,AddToCollectionForm
from VieseerApp.models import Image, Collection,CollectionImage,Tag
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

#Загрузка изображений
@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.author = request.user
            
            tags = form.cleaned_data['tags']
            if tags:
                tags_list = [tag.strip() for tag in tags.split(',')]
                tags_list = list(set(tags_list))
                new_image.tags = ', '.join(tags_list)
            
            new_image.save()
            return redirect('gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def gallery(request):
    tag_filter = request.GET.get('tag')
    
    # Оптимизированный запрос с предзагрузкой
    images = Image.objects.prefetch_related(
        Prefetch('collectionimage_set', 
                queryset=CollectionImage.objects.select_related('collection'),
                to_attr='user_collections')
    ).order_by('-uploaded_at')
    
    if tag_filter:
        images = images.filter(tags__icontains=tag_filter)
    
    # Получаем все теги
    all_tags = set(tag for image in Image.objects.all() for tag in image.get_tags_list())
    
    # Получаем коллекции пользователя (если авторизован)
    user_collections = []
    if request.user.is_authenticated:
        user_collections = Collection.objects.filter(user=request.user).prefetch_related('images')
    
    return render(request, 'gallery.html', {
        'images': images,
        'user': request.user,
        'all_tags': sorted(all_tags),
        'current_tag': tag_filter,
        'user_collections': user_collections
    })

#Установка изображений
def download_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    if not image.image or not default_storage.exists(image.image.name):
        raise Http404("Файл изображения не найден")
    
    file_path = image.image.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{image.get_download_filename()}"'
    return response

@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            return JsonResponse({'status': 'ok', 'id': collection.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error'})

@require_POST
@login_required
def manage_collection(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    form = AddToCollectionForm(request.POST, user=request.user)
    
    if form.is_valid():
        CollectionImage.objects.filter(
            collection__user=request.user,
            image=image
        ).delete()
        
        # Добавляем в выбранные коллекции
        for collection in form.cleaned_data['collections']:
            CollectionImage.objects.get_or_create(
                collection=collection,
                image=image
            )
        
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@login_required
def user_collections(request):
    collections = Collection.objects.filter(user=request.user).prefetch_related('images')
    return render(request, 'collections.html', {
        'collections': collections
    })

@require_POST
@login_required
def like_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    user = request.user
    
    if image.likes.filter(id=user.id).exists():
        image.likes.remove(user)
        liked = False
    else:
        image.likes.add(user)
        liked = True
    
    return JsonResponse({
        'status': 'success',
        'likes': image.likes.count(),
        'liked': liked
    })

@require_POST
@login_required
def add_to_collection(request):
    image_id = request.POST.get('image_id')
    collection_id = request.POST.get('collection_id')
    
    if not image_id or not collection_id:
        return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)
    
    image = get_object_or_404(Image, id=image_id)
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    
    # Используем get_or_create для связи через промежуточную модель
    collection_image, created = CollectionImage.objects.get_or_create(
        collection=collection,
        image=image
    )
    
    if not created:
        collection_image.delete()
        added = False
    else:
        added = True
    
    return JsonResponse({
        'status': 'success',
        'added': added,
        'collection_name': collection.name
    })
def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    user_collections = []
    
    if request.user.is_authenticated:
        user_collections = Collection.objects.filter(user=request.user)
    
    return render(request, 'image_detail.html', {
        'image': image,
        'user_collections': user_collections
    })