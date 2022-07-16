from django.shortcuts import render
from .models import customerAddress,customer,city
from django.http import  JsonResponse
import pytz

utc=pytz.UTC
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
    print(nm[1])
    nowTime=datetime.now().strftime("%Y%m%d%H%M%S")
    if nowTime>=nm[1]:
        title="Expired !!"
        status="Email Verification Link Expire!"
        icons="error"
    else:

        if data.count()==0:
            title="Verified!!"
            status="Already Verified !!"
            icons="success"
        else:
            title="Verified!!"
            status="Email Verification Successfully......!!!"
            icons="success"
                
    if icons=="success":
        customer.objects.filter(firstName=nm[0]).update(emailVarificationDate=datetime.now())
    return render(request,"doneVerify.html",{"title":title,"status":status,"icons":icons})

def getcitiesajax(request):
    if request.method == "POST":
        stateName = request.POST['statename']
        cities = city.objects.all().filter(stateName=stateName)
        
        return JsonResponse(list(cities.values('cityId', 'cityName')), safe = False)  



