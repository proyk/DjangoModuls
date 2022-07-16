from asyncio.windows_events import NULL
from turtle import title, update
from django.contrib import admin
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from pages.models import page
from languages.models import language
from translationPage.models import content
from .forms import PageForm,ContentForm
class ContentInline(admin.StackedInline):
    model = content
    extra = 1
    max_num = language.objects.count()
    list_display = ['language','page','title','content']



class PageAdmin(admin.ModelAdmin):
    list_display = ['slug','customCreatedAt','customUpdatedAt']
    def customCreatedAt(self,obj):
        return obj.created_at.strftime(settings.DATETIME_FORMAT)
    customCreatedAt.short_description="Created At"
    def customUpdatedAt(self,obj):
        return obj.updated_at.strftime(settings.DATETIME_FORMAT)
    customUpdatedAt.short_description="Updated At"
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        global pages
        
        if request.method=="POST":
            if "updateContent" in request.POST:
                pageForm=PageForm(request.POST,instance=pages)
                slugData=request.POST.get("slug")
                pageData=page.objects.filter(id=obj_id)
                
                langs=language.objects.all()
                for lang in langs:
                    titleData=request.POST.get(lang.title+"title")
                    contentData=request.POST.get(lang.title+"content")
                    updateContent=content.objects.get(contentId=request.POST.get(lang.title+'id'))
                    updateContent.page=pageData.get()
                    updateContent.language=lang
                    updateContent.title=titleData
                    updateContent.content=contentData
                    updateContent.save()
                pageForm.save()
                messages.success(request,"Data Updated successfully !!!!!")
                return HttpResponseRedirect('/admin/pages/page/')
            else:
                slugData=request.POST.get("slug")
                
                pageForm=PageForm(request.POST)
                pageForm.save()
                
                pageData=page.objects.filter(slug=slugData)
                langs=language.objects.all()
                for lang in langs:
                    
                    titleData=request.POST.get(lang.title+"title")
                    contentData=request.POST.get(lang.title+"content")
                    
                    if titleData!='' or contentData!='':
                        saveContent=content()
                        saveContent.page=pageData.get()
                        saveContent.language=lang
                        saveContent.title=titleData
                        saveContent.content=contentData
                        saveContent.save()
                        messages.success(request,lang.title+" Data Inserted successfully !!!!!")
                    

                    else:
                        messages.error(request,lang.title+" Not Inserted..........!")
                return HttpResponseRedirect('/admin/pages/page/')

            
        label="add"
        if obj_id==None:
            pageForm=PageForm()
            contentForm=ContentForm()
            languages = language.objects.filter(status="enabled")
            return super().changeform_view(request, obj_id, form_url,{'label':label,'pageForm':pageForm,'languages':languages,'contentForm':contentForm})
        else:
            label="update"
            pages=page.objects.get(id=obj_id)
            languages = language.objects.filter(status="enabled")
            initial_dict={}
            
            pagedetails = content.objects.raw(" select * from translationPage_content join pages_page on translationPage_content.page_id=pages_page.id where pages_page.id='"+obj_id+"'")
            print(pagedetails)
            
            

            
            pageForm=PageForm(instance=pages)
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'PageData':pagedetails,'pageForm':pageForm})
        
    
        
# Register your models here.
admin.site.register(page,PageAdmin)
