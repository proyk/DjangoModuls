from django.db import models
from django.db import transaction

# Create your models here.
class group(models.Model):
    groupId=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,verbose_name="Name")
    isDefault = models.BooleanField(default=False,verbose_name="Is Default")
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(group, self).save(*args, **kwargs)
        with transaction.atomic():
            group.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(group, self).save(*args, **kwargs)
    def __str__(self) :
        return self.name

def get_group():
    return group.objects.get(isDefault=True)

    
class customer(models.Model):
    customerId = models.AutoField(primary_key=True)
    firstName = models.CharField(('First Name'), max_length=100)
    lastName = models.CharField(('Last Name'), max_length=100)
    contactNo = models.CharField(('Mobile Number'),max_length=10, null=False, blank=False, unique=True)
    email = models.EmailField(('email Id'),null=False, blank=False, unique=True)
    profileImage = models.ImageField(('Profile Image'),upload_to='images/')
    password = models.CharField(("Password"),max_length=250)
    customerGroup = models.ForeignKey(group,on_delete=models.CASCADE,null=False,default=get_group)
    emailVarificationDate = models.DateTimeField(default=None,null=True,blank=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstName
class state(models.Model):
    stateId = models.AutoField(primary_key=True)
    stateName = models.CharField(("State Name"),max_length=24,unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stateName

class city(models.Model):
    cityId = models.AutoField(primary_key=True)
    stateName = models.ForeignKey('State',on_delete=models.CASCADE,null=True)
    cityName = models.CharField(("City Name"),max_length=24,unique=True)
    
    def __str__(self):
        return self.cityName

class customerAddress(models.Model):
    customerAddressId = models.AutoField(primary_key=True)
    addressName = models.CharField(('Name'),max_length=100)
    building = models.CharField(('Building / House No.'),max_length=200)
    street = models.CharField(('Street'),max_length=200)
    postalCode = models.IntegerField(('Postal Code'))
    landMark = models.CharField(('Landmark'),max_length=200)
    isDefault = models.BooleanField(("Is Default"),default=False)
    city = models.ForeignKey(city,on_delete=models.CASCADE,null=False)
    state = models.ForeignKey(state,on_delete=models.CASCADE,null=False)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE,null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.addressName