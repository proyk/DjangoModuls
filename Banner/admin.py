from email.mime import image
from django.contrib import admin
from .models import *
from .forms import *
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from languages.models import language
from django.utils.html import format_html
# Register your models here.
class BannerGroupAdmin(admin.ModelAdmin):
    list_display=["code","labelsOfGroups","enabledOrNot",'customCreatedAt','customUpdatedAt']
    def customCreatedAt(self,obj):
        return obj.created_at.strftime(settings.DATETIME_FORMAT)
    customCreatedAt.short_description="Created At"
    def customUpdatedAt(self,obj):
        return obj.updated_at.strftime(settings.DATETIME_FORMAT)
    customUpdatedAt.short_description="Updated At"
    def labelsOfGroups(self,obj):
        data=BannerGroupTranslation.objects.filter(bannerGroup_id=obj.BannerGroupId)
        str=""
        for i in data:
            str+=i.name+"-<strong>"+i.language_id+"</strong><br>"
        return format_html(str)
    labelsOfGroups.short_description="Lables (Language Wise)"
    def enabledOrNot(self,obj):
        if obj.status=="enabled":
            return format_html(f'<i class="ml-2 fas fa-check ">')
        else:
            return format_html(f'<i class="ml-2 fas fa-times ">')
    enabledOrNot.short_description="Enabled/Disbled"
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        global bannerGroups,banner
        
        if request.method=="POST":
            if "updateContent" in request.POST:
                bannerGroupForm=BannerGroupForm(request.POST,instance=bannerGroups)
                codeData=request.POST.get("code")
                bannerGroupData=BannerGroup.objects.filter(BannerGroupId=obj_id)
                
                langs=language.objects.all()
                for lang in langs:
                    nameData=request.POST.get(lang.title+"name")
                    
                    updateContent=BannerGroupTranslation.objects.get(BannerGroupTranslationId=request.POST.get(lang.title+'id'))
                    updateContent.bannerGroup=bannerGroupData.get()
                    updateContent.language=lang
                    updateContent.name=nameData
                    
                    updateContent.save()
                bannerGroupForm.save()
                messages.success(request,"Data Updated successfully !!!!!")
                return HttpResponseRedirect('/admin/Banner/bannergroup/')
            else:
                codeData=request.POST.get("code")
                
                bannerGroupForm=BannerGroupForm(request.POST)
                bannerGroupForm.save()
                
                BannerData=BannerGroup.objects.filter(code=codeData)
                langs=language.objects.all()
                for lang in langs:
                    
                    nameData=request.POST.get(lang.title+"name")
                    
                    
                    if nameData!='':
                        saveContent=BannerGroupTranslation()
                        saveContent.bannerGroup=BannerData.get()
                        saveContent.language=lang
                        saveContent.name=nameData
                        
                        saveContent.save()
                        messages.success(request,lang.title+" Data Inserted successfully !!!!!")
                    

                    else:
                        messages.error(request,lang.title+" Not Inserted..........!")
                return HttpResponseRedirect('/admin/Banner/bannergroup/')

            
        label="add"
        if obj_id==None:
            bannerGroupForm=BannerGroupForm()
            bannerTranslationForm=BannerGroupTranslationForm()

            languages = language.objects.filter(status="enabled")
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'bannerGroupForm':bannerGroupForm,'bannerTranslationForm':bannerTranslationForm})
        else:
            label="update"
            bannerGroups=BannerGroup.objects.get(BannerGroupId=obj_id)
            languages = language.objects.filter(status="enabled")
            bannerGroupForm=BannerGroupForm(instance=bannerGroups)
            BannerGroupDetails = BannerGroupTranslation.objects.raw(" select * from banner_bannergrouptranslation as bgt join banner_bannergroup as bg on bgt.bannerGroup_id=bg.BannerGroupId where bg.BannerGroupId='"+obj_id+"'")
            
            
            

            
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'bannerGroupForm':bannerGroupForm,'BannerGroupData':BannerGroupDetails})
        
class BannerAdmin(admin.ModelAdmin):
    list_display=["BannerId","labelsOfBanners","enabledOrNot","groupsWithImage",'customCreatedAt','customUpdatedAt']
    def customCreatedAt(self,obj):
        return obj.created_at.strftime(settings.DATETIME_FORMAT)
    customCreatedAt.short_description="Created At"
    def customUpdatedAt(self,obj):
        return obj.updated_at.strftime(settings.DATETIME_FORMAT)
    customUpdatedAt.short_description="Updated At"
    def enabledOrNot(self,obj):
        if obj.status=="enabled":
            return format_html(f'<i class="ml-2 fas fa-check ">')
        else:
            return format_html(f'<i class="ml-2 fas fa-times ">')
    enabledOrNot.short_description="Enabled/Disbled"
    def groupsWithImage(self,obj):
        data=BannerImage.objects.filter(Banner_id=obj.BannerId)
        str=""
        for i in data:
            str+="<img src=/media/images/"+i.image.name+" height=75 width=75 class='listImage' style='margin:15px;' />"
        return format_html(str)
    groupsWithImage.short_description="Images of Banners(G)"
    def labelsOfBanners(self,obj):
        data=BannerTranslation.objects.filter(Banner_id=obj.BannerId)
        str=""
        for i in data:
            str+=i.title+"-<strong>"+i.language_id+"</strong><br>"
        return format_html(str)
    labelsOfBanners.short_description="Lables (Language Wise)"
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        global banner,bImages
        
        if request.method=="POST":
            if "updateContent" in request.POST:
                banner=Banner.objects.get(BannerId=obj_id)
                bannerForm=BannerForm(request.POST,instance=banner)
                codeData=request.POST.get("code")
                bannerData=Banner.objects.get(BannerId=obj_id)
                bg=BannerGroup.objects.all()
                Existcount=bg.count()
                i=0
                for data in bg:
                    if request.FILES.get(data.code+"image")!=None:
                        BannerImage.objects.filter(BannerImageId=request.POST.get(data.code+"updateImageId")).update(
                        image=request.FILES.get(data.code+"image"),
                        url=request.POST.get(data.code+"url"),
                        )
                    
                    else:
                        BannerImage.objects.filter(BannerImageId=request.POST.get(data.code+"updateImageId")).update(
                        
                        url=request.POST.get(data.code+"url"),
                        
                        )
                    if request.POST.get(data.code+"updateImageId")==None:
                        BannerImage.objects.filter(BannerGroup_id=data.BannerGroupId).filter(Banner_id=obj_id).delete()
                    
                
                if int(request.POST.get("countData"))!=0:
                    
                    for i in range(0,int(request.POST.get("countData"))):
                        print(request.POST.get("bannergrpid["+str(i)+"]"))
                        if request.POST.get("bannergrpid["+str(i)+"]")==None:
                            print(i)
                        else:

                            bannerImageData=BannerImage()
                            bannerImageData.Banner=bannerData
                            bannerImageData.BannerGroup=BannerGroup.objects.get(BannerGroupId=request.POST.get("bannergrpid["+str(i)+"]"))
                            bannerImageData.image=request.FILES["bannerimage["+str(i)+"]"].name
                            bannerImageData.url=request.POST["url["+str(i)+"]"]
                            bannerImageData.save()
                langs=language.objects.all()
                for lang in langs:
                    titleData=request.POST.get(lang.title+"title")
                    contentData=request.POST.get(lang.title+"content")
                    
                    updateContent=BannerTranslation.objects.get(BannnerTransId=request.POST.get(lang.title+'id'))
                    updateContent.title=titleData
                    updateContent.language=lang
                    updateContent.content=contentData
                    updateContent.Banner=bannerData
                    updateContent.save()
                bannerForm.save()
                messages.success(request,"Data Updated successfully !!!!!")
                return HttpResponseRedirect('/admin/Banner/banner/')
            else:
                
                
                bannerForm=BannerForm(request.POST)
                bannerForm.save()
                print("---------")
                BannerData=Banner.objects.latest('BannerId')
                for i in range(0,int(request.POST["countData"])):

                    bannerImageData=BannerImage()
                    bannerImageData.Banner=BannerData
                    bannerImageData.BannerGroup=BannerGroup.objects.get(BannerGroupId=request.POST["bannergrpid["+str(i)+"]"])
                    bannerImageData.image=request.FILES["bannerimage["+str(i)+"]"]
                    bannerImageData.url=request.POST["url["+str(i)+"]"]
                    bannerImageData.save()
                    
                    #BannerData=BannerGroup.objects.filter(code=codeData)
                langs=language.objects.all()
                for lang in langs:
                    
                    titleData=request.POST.get(lang.title+"title")
                    contentData=request.POST.get(lang.title+"content")
                    
                    
                    if titleData!='' or contentData!='':
                        saveContent=BannerTranslation()
                        saveContent.title=titleData

                        saveContent.language=lang
                        saveContent.content=contentData
                        saveContent.Banner=BannerData
                        
                        saveContent.save()
                        messages.success(request,lang.title+" Data Inserted successfully !!!!!")
                    

                    else:
                        messages.error(request,lang.title+" Not Inserted..........!")
                    
                return HttpResponseRedirect('/admin/Banner/banner/')

            
        label="add"
        if obj_id==None:
            bannerForm=BannerForm()
            bannerTranslationForm=BannerTransForm()
            bannerImage=BannerImageForm()
            languages = language.objects.filter(status="enabled")
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'bannerForm':bannerForm,'bannerTranslationForm':bannerTranslationForm,'BannerImageForm':bannerImage})
        else:
            label="update"
            banner=Banner.objects.get(BannerId=obj_id)
            languages = language.objects.filter(status="enabled")
            bannerForm=BannerForm(instance=banner)
            BannerDetails = BannerTranslation.objects.filter(Banner_id=obj_id)
            bImages=BannerImage.objects.raw("select * from banner_bannerimage as bi join banner_bannergroup as bg on bi.BannerGroup_id=bg.BannerGroupId where Banner_id="+obj_id+"")
            
            
            

            
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'bannerForm':bannerForm,'BannerData':BannerDetails,'BannerImageForm':bImages})

admin.site.register(BannerGroup,BannerGroupAdmin)
admin.site.register(Banner,BannerAdmin)
