from django.db import models
from django.urls import reverse
# Create your models here.
class page(models.Model):
    slug = models.SlugField(primary_key=True, unique=True)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    sortOrder = models.IntegerField(default=0)
    

    def __str__(self):
        return str(self.slug)   


def get_page():
    return page.objects.get(sortOrder=1)
def get_absolute_url(self):
        return reverse("pages", kwargs={"slug": self.slug}) 