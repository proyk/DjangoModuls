from time import time
from django.contrib import admin
from django.conf import settings
from .models import group,customer,city,state,customerAddress
from .forms import CustomerForm,addressForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import cryptocode as c
# Register your models here.
class groupAdmin(admin.ModelAdmin):
    list_display=['name','isDefault']
class customerAdmin(admin.ModelAdmin):
    list_display=["name","email","profileImages","isVerified" ,"customerGroup","customCreatedAt","customUpdatedAt"]
    def name(self,obj):
        return obj.firstName+" "+obj.lastName
    def isVerified(self,obj):
        if obj.emailVarificationDate==None:
            return format_html(f'<i class="ml-2 fas fa-times ">')
        else:
            return format_html(f'<i class="ml-2 fas fa-check ">')
    def customCreatedAt(self,obj):
        return obj.createdAt.strftime(settings.DATETIME_FORMAT)
    customCreatedAt.short_description="Created At"
    def customUpdatedAt(self,obj):
        return obj.updatedAt.strftime(settings.DATETIME_FORMAT)
    customUpdatedAt.short_description="Updated At"
    isVerified.short_description ="Is Verified ?"
    def profileImages(self,obj):
        return format_html(f'<img src="/media/{obj.profileImage}" style="height:40px;width:40px">')
    profileImages.short_description="Profile Image"
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        if request.method=="POST":
            try:
                if "updateContent" in request.POST:
                    oldData=customer.objects.filter(customerId=obj_id)
                    for i in oldData:
                        if i.email==request.POST["email"]:
                            print(i.email)
                        else:

                            customer.objects.filter(customerId=obj_id).update(emailVarificationDate=None)
                            number = (datetime.now()+timedelta(minutes=15)).strftime("%Y%m%d%H%M%S")
                            code=request.POST["firstName"]+"-"+str(number)
                            html_content = render_to_string("emailverify.html",{'fname':request.POST["firstName"],"lname":request.POST["lastName"],'code':code})
                            text_content = strip_tags(html_content)
                            email = EmailMultiAlternatives(
                            "Email Verify Link",
                            text_content,
                            settings.EMAIL_HOST_USER,
                            [request.POST["email"]],
                            )
                            email.attach_alternative(html_content,"text/html")
                            email.send()
                    #print(data)
                    data=customer.objects.get(customerId=obj_id)
                    data.firstName=request.POST["firstName"]
                    data.lastName=request.POST["lastName"]
                    data.contactNo=request.POST["contactNo"]
                    data.email=request.POST["email"]
                    data.profileImage=request.FILES["profileImage"]
                    data.password=c.encrypt(request.POST["password"],"yk")
                    data.customerGroup=group.objects.get(groupId=request.POST["customerGroup"])
                    data.save()
                    if request.POST["updateContent"]=="Save":

                        if request.POST["addressName"]=="":
                            pass
                        else:
                            
                            addressData=customerAddress()
                            addressData.addressName=request.POST["addressName"]
                            addressData.building=request.POST["building"]
                            addressData.street=request.POST["street"]
                            addressData.postalCode=request.POST["postalCode"]
                            addressData.landMark=request.POST["landMark"]
                            if  request.POST.get('isDefault',None)=="on":
                                addressData.isDefault=True
                                customerAddress.objects.filter(customer=customer.objects.get(customerId=obj_id)).update(isDefault=False)
                            else:
                                addressData.isDefault=False
                            addressData.customer=customer.objects.get(customerId=obj_id)
                            addressData.state=state.objects.get(stateId=request.POST["state"])
                            addressData.city=city.objects.get(cityId=request.POST["city"])
                            addressData.save()
                    if request.POST["updateContent"]=="Update":
                        
                        if request.POST["addressName"]=="":
                            pass
                        else:
                            isDefault=False
                            if request.POST.get('isDefault',None)=="on":
                                isDefault=True
                                customerAddress.objects.filter(customer=customer.objects.get(customerId=obj_id)).update(isDefault=False)
                            else:

                                isDefault=False
                            addressUpdateData=customerAddress.objects.filter(customerAddressId=request.POST["updateId"]).update(
                            building=request.POST["building"],
                            addressName=request.POST["addressName"],
                            street=request.POST["street"],
                            postalCode=request.POST["postalCode"],
                            landMark=request.POST["landMark"],
                            isDefault=isDefault,
                            customer=customer.objects.get(customerId=obj_id),
                            state=state.objects.get(stateId=request.POST["state"]),
                            city=city.objects.get(cityId=request.POST["city"])

                            )
                    if "counter" in request.POST: 

                        for i in range(1,int(request.POST["counter"])+1):
                            addressData=customerAddress()
                            addressData.addressName=request.POST["Address["+str(i)+"][addressname]"]
                            addressData.building=request.POST["Address["+str(i)+"][building]"]
                            addressData.street=request.POST["Address["+str(i)+"][street]"]
                            addressData.postalCode=request.POST["Address["+str(i)+"][postalCode]"]
                            addressData.landMark=request.POST["Address["+str(i)+"][landMark]"]
                            
                            if  request.POST.get('Address['+str(i)+'][isDefault]',None)=="on":
                                addressData.isDefault=True
                                customerAddress.objects.filter(customer=customer.objects.get(customerId=obj_id)).update(isDefault=False)
                            else:
                                addressData.isDefault=False
                                addressData.customer=customer.objects.get(customerId=obj_id)
                                addressData.state=state.objects.get(stateId=request.POST["Address["+str(i)+"][state]"])
                                addressData.city=city.objects.get(cityId=request.POST["Address["+str(i)+"][city]"])
                                addressData.save()   
                    else:
                        messages.success(request,"Updated successfully !!!!!")
                    return HttpResponseRedirect('/admin/customers/customer/')
                else:
                    customerData=customer()
                    addressData=customerAddress()
                    customerData.firstName=request.POST["firstName"]
                    customerData.lastName=request.POST["lastName"]
                    customerData.contactNo=request.POST["contactNo"]
                    customerData.email=request.POST["email"]
                    customerData.profileImage=request.FILES["profileImage"]
                    customerData.password=c.encrypt(request.POST["password"],"yk")
                    customerData.customerGroup=group.objects.get(groupId=request.POST["customerGroup"])
                    
                        
                    customerData.save()
                    number = (datetime.now()+timedelta(minutes=15)).strftime("%Y%m%d%H%M%S")
                    code=request.POST["firstName"]+"-"+str(number)
                    html_content = render_to_string("emailverify.html",{'fname':request.POST["firstName"],"lname":request.POST["lastName"],'code':code})
                    text_content = strip_tags(html_content)
                    email = EmailMultiAlternatives(
                    "Email Verify Link",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [request.POST["email"]],
                    )
                    email.attach_alternative(html_content,"text/html")
                    email.send()
                    
                    addressData.addressName=request.POST["addressName"]
                    addressData.building=request.POST["building"]
                    addressData.street=request.POST["street"]
                    addressData.postalCode=request.POST["postalCode"]
                    addressData.landMark=request.POST["landMark"]
                    if request.POST.get('isDefault',None)=="on":
                        addressData.isDefault=True
                    else:
                        addressData.isDefault=False

                    addressData.customer=customer.objects.latest('createdAt')
                    addressData.state=state.objects.get(stateId=request.POST["state"])
                    addressData.city=city.objects.get(cityId=request.POST["city"])
                    addressData.save()
                    messages.success(request," Data "+request.POST["firstName"]+" & "+request.POST["addressName"]+" Inserted successfully !!!!!")
                    return HttpResponseRedirect('/admin/customers/customer/')

            except Exception as e:

                messages.error(request,e)
            
                
        label = "add"
        if obj_id==None:
            customerForm=CustomerForm()
            addressform=addressForm()
            return super().changeform_view(request, obj_id, form_url,{'lbl':label,'customerForm':customerForm,'addForm':addressForm})
        else:
            label="Update"
            
            customerId=customer.objects.get(customerId=obj_id)
            addressData=customerAddress.objects.filter(customer_id=obj_id)
            customerForm=CustomerForm()
            states=state.objects.all()
            AddressForm=addressForm()
            CustomerData=customer.objects.filter(customerId=obj_id)
            passData=""
            for i in CustomerData:
                passData=c.decrypt(i.password,"yk")
            
            return super().changeform_view(request, obj_id, form_url,{'lbl':label,'CustomerData':CustomerData,'passData':passData,'states':states,'customerForm':customerForm,'addForm':AddressForm,'addressData':addressData})
admin.site.register(group,groupAdmin)
admin.site.register(customer,customerAdmin)


