from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# 게시물 작성할때 들어갈 내용 : 제목, 내용, 위도, 경도, 이미지, 공개유무
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20) # 제목
    pub_date = models.DateTimeField('date published') # 작성 시간
    content = models.TextField() # 내용
    image = models.ImageField(upload_to='images/', blank=True) # 사진
    latitude = models.FloatField() # 위도
    longtitude = models.FloatField() # 경도
    public = models.BooleanField(default=False) #공개 유무
    
    def __str__(self):
        return self.title
        
    def summary(self):
        return self.content[:30]
