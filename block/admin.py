
from django.contrib import admin
from django.conf import settings

from block.forms import BlockContentForm, BlockForm
from .models import block, blockContent

from django.contrib import messages
from django.http import HttpResponseRedirect
from languages.models import language
# Register your models here.
class BlockAdmin(admin.ModelAdmin):
    list_display=["slug",'customCreatedAt','customUpdatedAt']
    def customCreatedAt(self,obj):
        return obj.created_at.strftime(settings.DATETIME_FORMAT)
    customCreatedAt.short_description="Created At"
    def customUpdatedAt(self,obj):
        return obj.updated_at.strftime(settings.DATETIME_FORMAT)
    customUpdatedAt.short_description="Updated At"
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        global blocks
        
        if request.method=="POST":
            if "updateContent" in request.POST:
                blockForm=BlockForm(request.POST,instance=blocks)
                slugData=request.POST.get("slug")
                blockData=block.objects.filter(blockId=obj_id)
                
                langs=language.objects.all()
                for lang in langs:
                    titleData=request.POST.get(lang.title+"title")
                    contentData=request.POST.get(lang.title+"content")
                    updateContent=blockContent.objects.get(blockContentId=request.POST.get(lang.title+'id'))
                    updateContent.block=blockData.get()
                    updateContent.language=lang
                    updateContent.title=titleData
                    updateContent.content=contentData
                    updateContent.save()
                blockForm.save()
                messages.success(request,"Data Updated successfully !!!!!")
                return HttpResponseRedirect('/admin/block/block/')
            else:
                slugData=request.POST.get("slug")
                
                blockForm=BlockForm(request.POST)
                blockForm.save()
                
                blockData=block.objects.filter(slug=slugData)
                langs=language.objects.all()
                for lang in langs:
                    
                    titleData=request.POST.get(lang.title+"title")
                    contentData=request.POST.get(lang.title+"content")
                    
                    if titleData!='' or contentData!='':
                        saveContent=blockContent()
                        saveContent.block=blockData.get()
                        saveContent.language=lang
                        saveContent.title=titleData
                        saveContent.content=contentData
                        saveContent.save()
                        messages.success(request,lang.title+" Data Inserted successfully !!!!!")
                    

                    else:
                        messages.error(request,lang.title+" Not Inserted..........!")
                return HttpResponseRedirect('/admin/block/block/')

            
        label="add"
        if obj_id==None:
            blockForm=BlockForm()
            blockContentForm=BlockContentForm()

            languages = language.objects.filter(status="enabled")
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'blockForm':blockForm,'blockContentForm':blockContentForm})
        else:
            label="update"
            blocks=block.objects.get(blockId=obj_id)
            languages = language.objects.filter(status="enabled")
            blockForm=BlockForm(instance=blocks)
            BlockDetails = blockContent.objects.raw(" select * from block_blockcontent as bc join block_block as bb on bb.blockId=bc.block_id where bb.blockId='"+obj_id+"'")
            
            
            

            
            return super().changeform_view(request, obj_id, form_url,{'label':label,'languages':languages,'blockForm':blockForm,'BlockData':BlockDetails})
        
    
admin.site.register(block,BlockAdmin)