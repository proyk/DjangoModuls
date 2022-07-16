from django import forms
from .models import block,blockContent

class BlockForm(forms.ModelForm):
    
    class Meta:
        model = block
        fields = ('status', 'slug') 
class BlockContentForm(forms.ModelForm):
    class Meta:
        model=blockContent
        fields=('language','title','content')