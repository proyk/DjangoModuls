
from django.contrib import admin
from django.utils.html import format_html
from .models import language

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title','locale','isDefault','status','created_at','updated_at']

# Register your models here.
admin.site.register(language,LanguageAdmin)