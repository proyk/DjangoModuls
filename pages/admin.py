from django.contrib import admin

from pages.models import page
from languages.models import language
from translationPage.models import content
class ContentInline(admin.StackedInline):
    model = content
    extra = 1
    max_num = language.objects.count()
    list_display = ['language','page','title','content']



class PageAdmin(admin.ModelAdmin):
    inlines = [ContentInline,]
    list_display = ['slug','status','sortOrder',]
# Register your models here.
admin.site.register(page,PageAdmin)