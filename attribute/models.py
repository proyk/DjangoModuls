from cProfile import label
from django.db import models


# Create your models here.
class AttributeFields(models.Model):
    attributeId = models.AutoField(primary_key=True)
    code =models.CharField(max_length=10,verbose_name="Code",unique=True)
    inputChoice = (
        ('boolean','Boolean'),
        ('checkbox','Checkbox'),
        ('multi-select','Multi-select'),
        ('select','Select'),
        ('radio','Radio'),
        ('textbox','Textbox'),
        ('textarea','Textarea'),
    )
    
    inputType = models.CharField(max_length=15,choices=inputChoice,default='enabled',verbose_name="Input Type")
    sortOrder=models.IntegerField(default=0,verbose_name="Sort Order")
    isRequired = models.BooleanField(default=False,verbose_name="Is Required?")
    def __str__(self):
        return str(self.code)
    


  