from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# 게시물 작성할때 들어갈 내용 : 제목, 내용, 위도, 경도, 이미지, 공개유무
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20) # 식당이름
    rating = models.FloatField() # 평점
    pub_date = models.DateTimeField('date published') # 작성 시간
    content = models.TextField() # 한줄평
    image = models.ImageField(upload_to='images/', blank=True) # 사진
    latitude = models.FloatField() # 위도
    longtitude = models.FloatField() # 경도
    # public = models.BooleanField(default=False) #공개 유무
    
    def __str__(self):
        return self.title
        
    def summary(self):
        return self.content[:30]


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) #유저랑 1:1관계
    name=models.CharField(max_length=10) #이름
    nickname=models.CharField(max_length=10) #닉네임
    gender = models.CharField(max_length=5) #성별
    birth = models.CharField(max_length=10) #생년월일
    image = models.ImageField(upload_to='images/',null=True, blank=True) #프로필 사진첨부

    def __str__(self):
        n_user=str(self.user)
        return n_user
 


@receiver(post_save, sender=User) #자동으로 생성
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()