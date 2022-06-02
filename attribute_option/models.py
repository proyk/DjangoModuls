from django.db import models
from django.db import transaction
from attribute.models import AttributeFields
from languages.models import language,get_language
# Create your models here.
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