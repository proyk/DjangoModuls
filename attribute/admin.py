from django.contrib import admin
from .models import AttributeFields
from attribute_translate.models import AttributeTranslate
from .forms import AttributeTranslateForm,AttributesFieldsForm
from languages.models import language
# Register your models here.
class AttributeFieldsAdmin(admin.ModelAdmin):
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        global attributeFields
        languageList=language.objects.filter(status='enabled')
        if request.method=="POST":
            
            if "updateContent" in request.POST:
                AttributesFieldsForm(request.POST,instance=attributeFields).save()
                attribute=AttributeFields.objects.get(code=request.POST.get("code"))
                for langs in languageList:
                    updateLabels=AttributeTranslate(attributeTranslateId=request.POST.get(langs.title+"id"))
                    updateLabels.fieldLabel=request.POST.get(langs.title+"fieldLabel")
                    updateLabels.languageId=langs
                    updateLabels.fieldId=attribute
                    updateLabels.save()
            else:
                AttributesFieldsForm(request.POST).save()
                attribute=AttributeFields.objects.get(code=request.POST.get("code"))
                for langs in languageList:
                    saveLabels=AttributeTranslate()
                    saveLabels.fieldLabel=request.POST.get(langs.title+"fieldLabel")
                    saveLabels.languageId=langs
                    saveLabels.fieldId=attribute
                    saveLabels.save()
                

        label="add"
        
        if obj_id==None:
            attributeTranslateForm=AttributeTranslateForm()
            
            attributeFieldsForm=AttributesFieldsForm()
            return super().changeform_view(request, obj_id, form_url,{'label':label,'attributeTranslateForm':attributeTranslateForm,'languageList':languageList,'attributeFieldsForm':attributeFieldsForm})
        else:
            label="update"
            attributeFields=AttributeFields.objects.get(attributeId=obj_id)
            attributeTranslateLabel=AttributeTranslate.objects.filter(fieldId=attributeFields)
            attributeFieldsForm=AttributesFieldsForm(instance=attributeFields)
            attributeTranslateForm=AttributeTranslateForm()
            return super().changeform_view(request, obj_id, form_url,{'label':label,'attributeTranslateLabel':attributeTranslateLabel,'attributeTranslateForm':attributeTranslateForm,'languageList':languageList,'attributeFieldsForm':attributeFieldsForm})
admin.site.register(AttributeFields,AttributeFieldsAdmin)