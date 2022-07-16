from django.db import models
from tinymce import models as tinymce_models
from languages.models import language,get_language
# Create your models here.
class block(models.Model):
    blockId = models.AutoField(primary_key=True)
    
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    slug = models.CharField(max_length=100,unique=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return str(self.slug) 
class blockContent(models.Model):
    blockContentId=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,default=None)
    content = tinymce_models.HTMLField()
    block = models.ForeignKey(block,on_delete = models.CASCADE,null=True)
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=True,default=get_language)
    