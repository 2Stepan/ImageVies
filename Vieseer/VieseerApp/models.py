from django.db import models
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