from django import forms

from .models import AttributeTranslate 
from .models import AttributeField
from .models import options,OptionTranslate
from django.forms import formset_factory
class AttributeTranslateForm(forms.ModelForm):
    
    class Meta:
        model = AttributeTranslate
        fields = ('fieldLabel', 'languageId') 
class AttributesFieldsForm(forms.ModelForm):
    class Meta:
        model=AttributeField
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

class optionTranslateForm(forms.ModelForm):
    class Meta:
        model=OptionTranslate
        fields=[
            'optionsLabel'
        ]
        widgets={
            'optionsLabel':forms.TextInput(attrs={'class':'formset-field'}),
        }
OptionTranslateFormSet=formset_factory(optionTranslateForm,extra=1)
AttributeOptionFormSet=formset_factory(AttributeOptionForm, extra=1)
