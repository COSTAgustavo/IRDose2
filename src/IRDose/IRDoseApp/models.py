from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator

from .validators import validate_O_1

User = settings.AUTH_USER_MODEL



# Create your models here.
class CumActivity(models.Model):
   owner    	= models.ForeignKey(User, on_delete = models.CASCADE)
   name      	= models.CharField(max_length=120)
   Organ     	= models.CharField(max_length=30, blank=False) # validators=[validate_O_1])
   t_1       	= models.FloatField(default=0.0, verbose_name='First time')
   A_1          = models.FloatField(default=0.0, verbose_name='First Activity')
   t_2       	= models.FloatField(default=0.0, verbose_name='Second time')
   A_2          = models.FloatField(default=0.0, verbose_name='Second Activity')
   t_3       	= models.FloatField(default=0.0, verbose_name='Third time')
   A_3       	= models.FloatField(default=0.0, verbose_name='Third Activity')
   t_4  	    = models.FloatField(default=0.0, verbose_name='Fourth time')
   A_4          = models.FloatField(default=0.0, verbose_name='Fourth Activity')
   CT_Patient   = models.FileField(null=True, blank=False, verbose_name='Patient CT', upload_to='../media/')
   CT_Organ     = models.FileField(null=True, blank=False, verbose_name='Source/target Organ', upload_to='../media/')
   CT_Target_1  = models.FileField(null=True, blank=True, verbose_name='Second Target Organ', upload_to='../media/')
   CT_Target_2  = models.FileField(null=True, blank=True, verbose_name='Third Target Organ', upload_to='../media/')
   slug         = models.SlugField(null=True, blank=True)
   timeStamp    = models.DateTimeField(auto_now_add=True)
   updated      = models.DateTimeField(auto_now=True)
   cumAct       = models.FloatField(default=-10.0)
   doseAbs      = models.FloatField(default=-10.0)

   location     = models.CharField(max_length=120, null=True, blank=True)
   category     = models.CharField(max_length=120, null=True, blank=True)
   NUCLIDE_CHOICES = (
      ('Lu', 'Lu-177'),
      ('I', 'I-131')
   )
   nuclidechoice = models.CharField(max_length=10, choices=NUCLIDE_CHOICES, default=NUCLIDE_CHOICES[0][0])

   #myDateField = models.DateTimeField(auto_now=False, auto_now_add=False)

   def __str__(self):
       return self.name

   def get_absolute_url(self):
      #return f"/IRDoseApp/{self.slug}"
      return reverse('IRDoseApp:infos', kwargs={'slug': self.slug})

   @property
   def title(self):
      return self.name


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
       instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=CumActivity)
