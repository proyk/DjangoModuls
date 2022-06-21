from django.db import models
from django.urls import reverse
# Create your models here.
class page(models.Model):
    id=models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    sortOrder = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return str(self.slug)   


def get_page():
    return page.objects.get(sortOrder=1)
def get_absolute_url(self):
        return reverse("pages", kwargs={"slug": self.slug}) 