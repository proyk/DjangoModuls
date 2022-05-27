from django.contrib import admin
from .models import AttributeTranslate
# Register your models here.
class AttributeTranslateAdmin(admin.ModelAdmin):
    list_per_page =5
    list_display = ['fieldLabel','languageId']
admin.site.register(AttributeTranslate,AttributeTranslateAdmin)