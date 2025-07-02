from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from VieseerApp.models import Image,Collection

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

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название коллекции',
                'class': 'form-control'
            })
        }

class AddToCollectionForm(forms.Form):
    collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['collections'].queryset = Collection.objects.filter(user=user)