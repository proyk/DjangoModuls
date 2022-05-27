from django.db import models
from languages.models import language,get_language
from attribute.models import AttributeFields
# Create your models here.
class AttributeTranslate(models.Model):
    attributeTranslateId=models.AutoField(primary_key=True)
    fieldLabel=models.CharField(max_length=15,verbose_name="Label")
    fieldId=models.ForeignKey(AttributeFields,on_delete=models.CASCADE,null=False)
    languageId=models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    def __str__(self):
        return str(self.fieldLabel)