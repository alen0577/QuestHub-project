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
    user=models.ForeignKey(Registerprofile,on_delete=models.CASCADE,default='',null=True,blank=True)
    question=models.TextField(null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)


class Answer(models.Model):
    user = models.ForeignKey(Registerprofile, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    likes = models.ManyToManyField(Registerprofile, related_name='like_answers', blank=True)

    def like_count(self):
        return self.likes.count()