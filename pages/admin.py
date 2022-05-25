from asyncio.windows_events import NULL
from django.contrib import admin

from pages.models import page
from languages.models import language
from translationPage.models import content
from .forms import PageForm
class ContentInline(admin.StackedInline):
    model = content
    extra = 1
    max_num = language.objects.count()
    list_display = ['language','page','title','content']



class PageAdmin(admin.ModelAdmin):
    
    
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        
        if obj_id==None:
            pageForm=PageForm()
            languages = language.objects.filter(status="enabled")
            return super().changeform_view(request, obj_id, form_url,{'pageForm':pageForm,'languages':languages})
        else:
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
            pageForm=PageForm(initial = initial_dict)
            return super().changeform_view(request, obj_id, form_url,{'languages':languages,'PageData':pagedetails,'pageForm':pageForm})
    
    
        
# Register your models here.
admin.site.register(page,PageAdmin)