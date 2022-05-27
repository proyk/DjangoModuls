from django import forms
from attribute_translate.models import AttributeTranslate 
from attribute.models import AttributeFields
class AttributeTranslateForm(forms.ModelForm):
    
    class Meta:
        model = AttributeTranslate
        fields = ('fieldLabel', 'languageId') 
class AttributesFieldsForm(forms.ModelForm):
    class Meta:
        model=AttributeFields
        fields=('code','inputType','attributeId','sortOrder','isRequired')