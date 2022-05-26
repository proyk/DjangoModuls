from asyncio.windows_events import NULL
from turtle import title
from django.contrib import admin

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
    
    
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        if request.method=="POST":
            if "updateContent" in request.POST:
                print("Updating")
            else:
                slugData=request.POST.get("slug")
                print(request.POST)
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
                    else:
                        print(lang.title+" Not Inserted..........!")
            
        label="add"
        if obj_id==None:
            pageForm=PageForm()
            contentForm=ContentForm()
            languages = language.objects.filter(status="enabled")
            return super().changeform_view(request, obj_id, form_url,{'label':label,'pageForm':pageForm,'languages':languages,'contentForm':contentForm})
        else:
            label="update"
            languages = language.objects.filter(status="enabled")
            initial_dict={}
            
            pagedetails = content.objects.raw(" select * from translationPage_content join pages_page on translationPage_content.page_id=pages_page.slug where pages_page.slug='"+obj_id+"'")
            
            pages=page.objects.filter(slug=obj_id)
            for i in pages:
                initial_dict = {
                    
                    "slug" : i.slug,
                    "status" : i.status,
                    "sortOrder":i.sortOrder
                   
                }

            for x in pagedetails:
                print(x.language_id)
            pageForm=PageForm(initial = initial_dict)
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'PageData':pagedetails,'pageForm':pageForm})
        
    
        
# Register your models here.
admin.site.register(page,PageAdmin)