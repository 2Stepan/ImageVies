from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from VieseerApp.models import Image

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"] 

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={
                'placeholder': 'тег1, тег2, тег3'
            })
        }