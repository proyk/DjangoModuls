from lib2to3.pgen2.token import OP
from django.contrib import admin
from .models import AttributeField
from .models import AttributeTranslate
from .forms import AttributeTranslateForm,AttributesFieldsForm
from languages.models import language
from .forms import AttributeOptionFormSet,AttributeOptionForm,OptionTranslateFormSet,optionTranslateForm
from .models import options
from .models import OptionTranslate
from django.forms import modelformset_factory
from django.db import  IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect


# Register your models here.
class AttributeFieldsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        fieldsData=AttributeField.objects.all()
        fieldsLabelData=AttributeTranslate.objects.all()
        customAttributesData=options.objects.all().order_by("sortOrder")
        customAttributesLabelsData=options.objects.raw("select * from customattributes_options as co join customattributes_optiontranslate as cot on co.optionId=cot.optionId_id")
        return super().changelist_view(request, {"fieldsData":fieldsData,"labelData":fieldsLabelData,'customAttributesData':customAttributesData,'customAttributesLabelsData':customAttributesLabelsData})
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        global attributeFields
        global errorLabel
        languageList=language.objects.filter(status='enabled')
        OptFormset = modelformset_factory(options, form=AttributeOptionForm)
        formset = OptFormset(request.POST or None, queryset= options.objects.none(), prefix="options")   
        OptionTranslateSet= modelformset_factory(OptionTranslate,form=optionTranslateForm)
        optionFormSet=OptionTranslateSet(request.POST or None, queryset= OptionTranslate.objects.none(), prefix="options")    
        if request.method=="POST":
            
            
            
            try:
                
                if "updateContent" in request.POST:
                    AttributesFieldsForm(request.POST,instance=attributeFields).save()
                    attribute=AttributeField.objects.get(code=request.POST.get("code"))
                    


                        
                    for langs in languageList:
                        updateLabels=AttributeTranslate(attributeTranslateId=request.POST.get(langs.title+"id"))
                        
                        updateLabels.fieldLabel=request.POST.get(langs.title+"fieldLabel")
                        updateLabels.languageId=langs
                        updateLabels.fieldId=attribute
                        updateLabels.save()
                    optionsData=options.objects.filter(fieldId_id=obj_id)
                    getInputType=AttributeField.objects.filter(code=request.POST.get("code"))
                    
                    for i in getInputType:
                        if i.inputType=="boolean" or i.inputType=="textbox" or i.inputType=="textarea":
                            options.objects.filter(fieldId=obj_id).delete()
                        else:
                            for i in optionsData:
                                validate="no"
                                for langs in languageList:
                                                                       
                                    updateOptionLabels=OptionTranslate(optionTranslateId=request.POST.get(str(i.optionId)+langs.locale+"OptionLabelid"))
                                    getOptionLabel=request.POST.get(str(i.optionId)+"-"+langs.locale)
                                    updateOptionLabels.optionsLabel=getOptionLabel
                                    updateOptionLabels.languageId=langs
                                    updateOptionLabels.optionId=i
                                    errorLabel=request.POST.get(str(i.optionId)+"customOption")
                                    updateOptionLabels.save()
                                    validate="yes"
                                if validate=="yes":
                                    updateCustomOption=options.objects.get(optionId=i.optionId)
                                    updateCustomOption.customOption=request.POST.get(str(i.optionId)+"customOption")
                                    updateCustomOption.sortOrder=request.POST.get(str(i.optionId)+"customSortOrder")
                                    if request.POST.get(str(i.optionId)+"customIsDefault")=="on":
                                        updateCustomOption.isDefault=True
                                    else:
                                        updateCustomOption.isDefault=False
                                    updateCustomOption.fieldId=attribute
                                    updateCustomOption.save()
                                
                            no_custom=0
                            for form in formset:
                                if len(form["customOption"].data)==0 :
                                    no_custom=1
                                else:
                                    data2=form.save(commit=False)
                                    data2.fieldId=attribute
                                    data2.save()
                                    
                            if request.POST.get("options-TOTAL_FORMS")!=None:
                                for i in range(0,int(request.POST.get("options-TOTAL_FORMS"))):
                                    for langs in languageList:
                                        getLable=request.POST.get(langs.locale+"options-"+str(i)+"-optionsLabel")
                                        
                                        if no_custom!=1:

                                            saveOptionTranslate=OptionTranslate()
                                            saveOptionTranslate.optionsLabel=getLable
                                            saveOptionTranslate.languageId=langs
                                            optionId=options.objects.get(customOption=request.POST.get("options-"+str(i)+"-customOption"))
                                            saveOptionTranslate.optionId=optionId
                                            errorLabel=request.POST.get("options-"+str(i)+"-customOption")
                                            saveOptionTranslate.save()
                                
                    
                else:
                    AttributesFieldsForm(request.POST).save()
                    attribute=AttributeField.objects.get(code=request.POST.get("code"))
                    for langs in languageList:
                        
                        saveLabels=AttributeTranslate()
                        saveLabels.fieldLabel=request.POST.get(langs.locale+"fieldLabel")
                        saveLabels.languageId=langs
                        saveLabels.fieldId=attribute
                        saveLabels.save()
                    no_custom=0
                    for form in formset:
                        
                        if len(form["customOption"].data)==0:
                            no_custom=1
                            
                        else:
                            data2=form.save(commit=False)
                            
                            data2.fieldId=attribute
                            data2.save()

                    for i in range(0,int(request.POST.get("options-TOTAL_FORMS"))):
                        for langs in languageList:
                            getLable=request.POST.get(langs.locale+"options-"+str(i)+"-optionsLabel")
                            
                            if no_custom!=1:

                                saveOptionTranslate=OptionTranslate()
                                saveOptionTranslate.optionsLabel=getLable
                                saveOptionTranslate.languageId=langs
                                optionId=options.objects.get(customOption=request.POST.get("options-"+str(i)+"-customOption"))
                                saveOptionTranslate.optionId=optionId
                                saveOptionTranslate.save()
                            
                    messages.success(request,"Data Inserted successfully !!!!!")
                    return HttpResponseRedirect('/admin/CustomAttributes/attributefields/')



                
                    
            
            except IntegrityError as e:
                messages.error(request,'"'+errorLabel+'" Contains Duplicate Values !!!')
                options.objects.get(customOption=errorLabel).delete()
                return HttpResponseRedirect('/admin/CustomAttributes/attributefields/'+str(obj_id)+'/change/')
            except ValueError as er:
                messages.error(request,'"'+errorLabel+'" Already Exists !')
                return HttpResponseRedirect('/admin/CustomAttributes/attributefields/'+str(obj_id)+'/change/')
            except NameError as ne:
                
                return HttpResponseRedirect('/admin/CustomAttributes/attributefields/'+str(obj_id)+'/change/')         

        label="add"
        
        if obj_id==None:
            attributeTranslateForm=AttributeTranslateForm()
            
            attributeFieldsForm=AttributesFieldsForm()
            return super().changeform_view(request, obj_id, form_url,{'label':label,'attributeTranslateForm':attributeTranslateForm,'languageList':languageList,'attributeFieldsForm':attributeFieldsForm,'formset': formset,'optionFormset':optionFormSet})
        else:
            label="update"
            attributeFields=AttributeField.objects.get(attributeId=obj_id)
            attributeTranslateLabel=AttributeTranslate.objects.filter(fieldId=attributeFields)
            attributeFieldsForm=AttributesFieldsForm(instance=attributeFields)
            attributeTranslateForm=AttributeTranslateForm()
            data=AttributeField.objects.raw("select attributeId,optionsLabel,optionTranslateId,code,optionId,customOption,attributeId,languageId_id from CustomAttributes_attributefields as at join customattributes_options as ao on at.attributeId=ao.fieldId_id join customattributes_optiontranslate as aot on ao.optionId=aot.optionId_id where at.attributeId="+obj_id+";")
            customData=options.objects.filter(fieldId_id=obj_id)
            no_data=True
            
            if len(data)==0 and len(customData)==0:
                no_data=False
            
                

            return super().changeform_view(request, obj_id, form_url,{'customData':customData,'no_data':no_data,'updateData':data,'label':label,'attributeTranslateLabel':attributeTranslateLabel,'attributeTranslateForm':attributeTranslateForm,'languageList':languageList,'attributeFieldsForm':attributeFieldsForm,'formset': formset,'optionFormset':optionFormSet})
class AttributeTranslateAdmin(admin.ModelAdmin):
    list_per_page =5
    list_display = ['fieldLabel','languageId']
admin.site.register(AttributeField,AttributeFieldsAdmin)
