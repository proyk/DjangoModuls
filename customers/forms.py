from django import forms
from .models import customer,customerAddress


class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = customer
        fields = ('firstName', 'lastName','contactNo','email','profileImage','password','customerGroup','emailVarificationDate') 
        
class addressForm(forms.ModelForm):
    class Meta:
        model=customerAddress
        fields=('addressName','building','street','postalCode','landMark','isDefault','city','state','customer')