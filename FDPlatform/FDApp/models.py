from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Camera(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    gps_position_x= models.FloatField(default=0,blank=False,null=False)
    gps_position_y= models.FloatField(default=0,blank=False,null=False)
    viewers=models.ManyToManyField(User,blank=True)
    def __str__(self):
        return self.name

class PlatformUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='profile_pics',blank=True,null=True,default='profile_pics/default.png')
    
    
    
class Stats(models.Model):
    name=models.CharField(max_length=50)
    date=models.DateField(auto_now_add=True)
    value=models.IntegerField(default=0)
    
class Visits(models.Model):
    date_time=models.DateField(auto_now_add=True)
    number_of_visits=models.IntegerField(default=0)
    
