from django.db import models
from tinymce import models as tinymce_models
from languages.models import language,get_language
from pages.models import page,get_page
# Create your models here.
class content(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    page = models.ForeignKey(page,on_delete = models.CASCADE,null=False)
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=False)
    content = tinymce_models.HTMLField(null=False)

    
    def __str__(self):
        return str(self.title)   