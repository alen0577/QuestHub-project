from django.db import models

# Create your models here.


class Registerprofile(models.Model):
    username=models.CharField(max_length=100,default='',null=True,blank=True)
    password=models.CharField(max_length=50,default='',null=True,blank=True)
    email=models.EmailField(max_length=50,default='sample@gmail.com',null=True,blank=True)
    log_date = models.DateField(auto_now_add=True,null=True)
    log_time = models.TimeField(auto_now_add=True,null=True)
    position = models.CharField(max_length=255,default='User',null=True,blank=True)
    is_staff = models.IntegerField(default=0)
    active_status = models.IntegerField(default=0)

class Questions(models.Model):
    user=models.ForeignKey(Registerprofile,on_delete=models.CASCADE, null=True,default='')
    question=models.TextField()
    date = models.DateField(auto_now_add=True,null=True)
    time = models.TimeField(auto_now_add=True,null=True)
