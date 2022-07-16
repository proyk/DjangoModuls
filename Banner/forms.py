from django import forms
from .models import *

class BannerGroupForm(forms.ModelForm):
    
    class Meta:
        model = BannerGroup
        fields = ('status', 'sort_order','code') 
class BannerGroupTranslationForm(forms.ModelForm):
    class Meta:
        model=BannerGroupTranslation
        fields=('language','bannerGroup','name')
class BannerForm(forms.ModelForm):
    class Meta:
        model=Banner
        fields=('sort_order','status','isFeatured','bannerGroups')
class BannerTransForm(forms.ModelForm):
    class Meta:
        model=BannerTranslation
        fields=('title','content','Banner')
class BannerImageForm(forms.ModelForm):
    class Meta:
        model=BannerImage
        fields=('Banner','BannerGroup','image','url')