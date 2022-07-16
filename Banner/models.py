from django.db import models

from languages.models import language,get_language
# Create your models here.
class BannerGroup(models.Model):
    BannerGroupId = models.AutoField(primary_key=True)
    
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    sort_order=models.IntegerField(default=0)
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    code = models.CharField(max_length=10,unique=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return str(self.code) 
class BannerGroupTranslation(models.Model):
    BannerGroupTranslationId=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default=None)
    bannerGroup = models.ForeignKey(BannerGroup,on_delete = models.CASCADE,null=True)
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=True,default=get_language)
    def __str__(self):
        return str(self.name)
class Banner(models.Model):
    BannerId=models.AutoField(primary_key=True)
    sort_order=models.IntegerField(default=0)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    isFeatured=models.BooleanField()
    bannerGroups = models.ManyToManyField(BannerGroup)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return str(self.BannerId)
    class Meta:
         verbose_name = "Banner List"
class BannerTranslation(models.Model):
    BannnerTransId=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,default=None)
    content=models.CharField(max_length=200,default=None)
    Banner=models.ForeignKey(Banner,on_delete = models.CASCADE,null=True)
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=True,default=get_language)
    def __str__(self):
        return str(self.title)

class BannerImage(models.Model):
    BannerImageId=models.AutoField(primary_key=True)
    Banner=models.ForeignKey(Banner,on_delete = models.CASCADE,null=True)
    BannerGroup=models.ForeignKey(BannerGroup,on_delete = models.CASCADE,null=True)
    image=models.ImageField(('Profile Image'),upload_to='bannerImage/')
    url=models.URLField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return str(self.BannerImageId)
