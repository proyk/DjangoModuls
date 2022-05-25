from django.shortcuts import render
from pages.models import page
from languages.models import language
from translationPage.models import content
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def page_list():
    pages = page.objects.filter(status="enabled").order_by('sortOrder')
    languages = language.objects.filter(status="enabled")
    
    return pages,languages

def pages(request,slug):
    pages,languages = page_list()
    
    no_data=False
    if "locale" in request.session:
        print(request.session["locale"])
        pagedetails = content.objects.raw("select * from translationPage_content inner join languages_language on translationPage_content.language_id=languages_language.locale where translationPage_content.page_id='"+slug+"' and languages_language.locale='"+request.session["locale"]+"'")
    if not "locale" in request.session:
        pagedetails = content.objects.raw("select * from translationPage_content inner join languages_language on translationPage_content.language_id=languages_language.locale where translationPage_content.page_id='"+slug+"' and languages_language.isDefault=1")
    
    if len(pagedetails)==0:
        no_data=True
    else:
        for i in pagedetails:
            request.session["locale"]=i.locale
    return render(request,'slugpage.html',{'page':pagedetails,'pages':pages,'languages':languages,"no_data":no_data})
def change_languages(request):
    if request.method == "POST":
        locale=request.POST['localeLanguage']
        request.session['locale'] = locale
        msg={
            "Tag":"Success",
        }
        return JsonResponse(msg)

