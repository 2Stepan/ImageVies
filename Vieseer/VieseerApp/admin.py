from django.contrib import admin
import os
from VieseerApp.models import Image

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    actions = ['delete_selected_with_files']

    def delete_selected_with_files(self, request, queryset):
        for obj in queryset:
            if obj.image:
                if os.path.isfile(obj.image.path):
                    os.remove(obj.image.path)
            obj.delete()
        self.message_user(request, "Изображения и файлы успешно удалены")

admin.site.register(Image, ImageAdmin)