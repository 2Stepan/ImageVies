from django.db import models
from PIL import Image as PILImage
from django.core.files.storage import default_storage
import os
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
class Image(models.Model):
    image = models.ImageField(upload_to='user_uploads/%Y/%m/%d/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, blank=True, verbose_name="Теги (через запятую)")
    resolution = models.CharField(max_length=20, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_images', blank=True)

    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()

    def get_tags_list(self):
        """Возвращает список тегов"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.resolution: 
            from PIL import Image as PILImage
            img = PILImage.open(self.image) 
            self.resolution = f"{img.width}x{img.height}" 
        super().save(*args, **kwargs)  

    def image_exists(self):
        """Проверяет существует ли файл изображения"""
        if not self.image:
            return False
        return default_storage.exists(self.image.name)

    def get_resolution(self):
        """Безопасное получение разрешения изображения"""
        if not self.image:
            return "Нет файла"
    
        try:
            if not os.path.exists(self.image.path):
                return "Файл удалён"
            
            with PILImage.open(self.image.path) as img:
                return f"{img.width}×{img.height} px"
        except:
            return "Ошибка определения"
    
    def get_download_filename(self):
        """Генерирует имя файла для скачивания"""
        base = os.path.basename(self.image.name)
        return f"{os.path.splitext(base)[0]}_{self.width}x{self.height}{os.path.splitext(base)[1]}"
    
    def get_collections_for_user(self, user):
        return Collection.objects.filter(
            collectionimage__image=self,
            user=user
        )
    
class Collection(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField('Image', through='CollectionImage')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CollectionImage(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('collection', 'image')