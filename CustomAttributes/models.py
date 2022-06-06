from django.db import models

# Create your models here.
from languages.models import language,get_language

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
    


class options(models.Model):
    optionId = models.AutoField(primary_key=True)
    customOption = models.CharField(("Custom Option"),max_length=100,unique=True)
    fieldId=models.ForeignKey(AttributeFields,on_delete=models.CASCADE,null=False)
    sortOrder = models.IntegerField(("Sort Order"),default=0)
    isDefault = models.BooleanField(("Is Default"),default=False)
    
    def __str__(self) -> str:
        return self.customOption

class OptionTranslate(models.Model):
    optionTranslateId=models.AutoField(primary_key=True)
    optionsLabel=models.CharField(max_length=10,verbose_name="Option Label",unique=True)
    languageId=models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    optionId=models.ForeignKey(options,on_delete = models.CASCADE,null=False)
    def __str__(self):
        return str(self.optionsLabel)
class AttributeTranslate(models.Model):
    attributeTranslateId=models.AutoField(primary_key=True)
    fieldLabel=models.CharField(max_length=15,verbose_name="Label")
    fieldId=models.ForeignKey(AttributeFields,on_delete=models.CASCADE,null=False)
    languageId=models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    def __str__(self):
        return str(self.fieldLabel)