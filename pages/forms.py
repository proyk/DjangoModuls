from django import forms
from .models import page
from translationPage.models import content

class PageForm(forms.ModelForm):
    
    class Meta:
        model = page
        fields = ('slug', 'status','sortOrder') 
class ContentForm(forms.ModelForm):
    class Meta:
        model=content
        fields=('language','page','title','content')