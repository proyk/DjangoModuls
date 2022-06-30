from django.shortcuts import render
from .models import customerAddress,customer
from django.http import  JsonResponse

from datetime import datetime
# Create your views here.
def delete(request):
    id = request.GET.get('id')
    print(id)
    i = customerAddress.objects.get(customerAddressId = id[:-1])
    i.delete()
    return JsonResponse("sucess", safe = False) 
def edit(request):
    id = request.GET.get('id')
    i = customerAddress.objects.all().filter(customerAddressId = id[:-1])
    return JsonResponse(list(i.values()),safe=False)
def verifyEmail(request):
    nm=request.GET["code"].split("-")
    data =customer.objects.filter(firstName=nm[0]).filter(emailVarificationDate=None)
    status=""
    if data.count()==0:
        status="Already Verified !!"
    else:
        status="Email Verification Successfully......!!!"
        customer.objects.filter(firstName=nm[0]).update(emailVarificationDate=datetime.now())
    return render(request,"doneVerify.html",{"status":status})