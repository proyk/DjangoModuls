from django import forms

from attribute_translate.models import AttributeTranslate 
from attribute.models import AttributeFields
from attribute_option.models import options
from django.forms import formset_factory
class AttributeTranslateForm(forms.ModelForm):
    
    class Meta:
        model = AttributeTranslate
        fields = ('fieldLabel', 'languageId') 
class AttributesFieldsForm(forms.ModelForm):
    class Meta:
        model=AttributeFields
        fields=('code','inputType','attributeId','sortOrder','isRequired')
class AttributeOptionForm(forms.ModelForm):
    class Meta:
        model=options
        fields=[
            'customOption',
            'sortOrder',
            'isDefault',
            ]
        widgets = {
			'customOption': forms.TextInput(attrs={'class': 'formset-field'}),
			'sortOrder': forms.NumberInput(attrs={'class': 'formset-field'}),
            'isDefault': forms.CheckboxInput(attrs={'class': 'formset-field'}),
		}

        

AttributeOptionFormSet=formset_factory(AttributeOptionForm, extra=1)
