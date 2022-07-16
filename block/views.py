from django.shortcuts import render
from .models import blockContent
# Create your views here.
def displayBlock(request):
    data=blockContent.objects.all()
    return render(request,"display.html",{"blockData":data})