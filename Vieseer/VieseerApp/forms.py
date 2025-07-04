from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from VieseerApp.models import Image,Collection,FORBIDDEN_WORDS

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
                'placeholder': 'тег'
            })
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if not tags:
            return tags
        
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        forbidden_found = []
    
        for tag in tag_list:
            lower_tag = tag.lower()
            if any(forbidden_word in lower_tag or 
               lower_tag in forbidden_word 
               for forbidden_word in FORBIDDEN_WORDS):
                print(tag)
                forbidden_found.append(tag)
    
        if forbidden_found:
            raise forms.ValidationError(
                f"Обнаружены запрещённые слова: {', '.join(forbidden_found)}"
            )
    
        return tags

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