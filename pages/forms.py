from django import forms
from .models import page

class PageForm(forms.ModelForm):
    
    class Meta:
        model = page
        fields = ('slug', 'status','sortOrder') 