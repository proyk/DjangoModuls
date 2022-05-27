from django.contrib import admin

from translationPage.models import content

# Register your models here.
class ContentAdmin(admin.ModelAdmin):
    model = content
    list_display = ['title','language','page',]
