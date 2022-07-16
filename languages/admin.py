
from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import language

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title','locale','isDefault','status','customCreatedAt','customUpdatedAt']
    def customCreatedAt(self,obj):
        return obj.created_at.strftime(settings.DATETIME_FORMAT)
    customCreatedAt.short_description="Created At"
    def customUpdatedAt(self,obj):
        return obj.updated_at.strftime(settings.DATETIME_FORMAT)
    customUpdatedAt.short_description="Updated At"

# Register your models here.
admin.site.register(language,LanguageAdmin)