from django.contrib import admin
from django.conf import settings
from .models import group,customer,city,state,customerAddress
from .forms import CustomerForm,addressForm
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random

# Register your models here.
class groupAdmin(admin.ModelAdmin):
    list_display=['name','isDefault']
class customerAdmin(admin.ModelAdmin):
    list_display=["name","email","profileImages","isVerified" ,"customerGroup","createdAt","updatedAt"]
    def name(self,obj):
        return obj.firstName+" "+obj.lastName
    def isVerified(self,obj):
        if obj.emailVarificationDate==None:
            return format_html(f'<i class="ml-2 fas fa-times ">')
        else:
            return format_html(f'<i class="ml-2 fas fa-check ">')
    isVerified.short_description ="Is Verified ?"
    def profileImages(self,obj):
        return format_html(f'<img src="/media/{obj.profileImage}" style="height:40px;width:40px">')
    profileImages.short_description="Profile Image"
    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        if request.method=="POST":
            try:
                if "updateContent" in request.POST:
                    if request.POST["updateContent"]=="Save":
                        
                        addressData=customerAddress()
                        addressData.addressName=request.POST["addressName"]
                        addressData.building=request.POST["building"]
                        addressData.street=request.POST["street"]
                        addressData.postalCode=request.POST["postalCode"]
                        addressData.landMark=request.POST["landMark"]
                        if request.POST["isDefault"]=="on":
                            addressData.isDefault=True
                            customerAddress.objects.filter(customer=customer.objects.get(customerId=obj_id)).update(isDefault=False)
                        else:
                            addressData.isDefault=False
                        addressData.customer=customer.objects.get(customerId=obj_id)
                        addressData.state=state.objects.get(stateId=request.POST["state"])
                        addressData.city=city.objects.get(cityId=request.POST["city"])
                        addressData.save()
                    if request.POST["updateContent"]=="Update":
                        isDefault=False
                        if request.POST["isDefault"]=="on":
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
                        
                        
                else:
                    customerData=customer()
                    addressData=customerAddress()
                    customerData.firstName=request.POST["firstName"]
                    customerData.lastName=request.POST["lastName"]
                    customerData.contactNo=request.POST["contactNo"]
                    customerData.email=request.POST["email"]
                    customerData.profileImage=request.FILES["profileImage"]
                    customerData.password=request.POST["password"]
                    customerData.customerGroup=group.objects.get(groupId=request.POST["customerGroup"])
                    
                        
                    customerData.save()
                    number = random.randint(1000,9999)
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
                    if request.POST["isDefault"]=="on":
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
            customerForm=CustomerForm(instance=customerId)

            AddressForm=addressForm()
            return super().changeform_view(request, obj_id, form_url,{'lbl':label,'customerForm':customerForm,'addForm':AddressForm,'addressData':addressData})
admin.site.register(group,groupAdmin)
admin.site.register(customer,customerAdmin)


