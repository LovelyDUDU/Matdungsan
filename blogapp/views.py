from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Blog, Profile
from django.contrib.auth.models import User
import ctypes

def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs})


def create(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'index.html')
    
        elif request.method =="POST":
            blog = Blog()
            blog.user = request.user
            blog.title = request.POST['title']
            blog.rating = request.POST['rating']
            blog.content = request.POST['content']
            blog.pub_date = timezone.datetime.now()
            try:
                blog.image=request.FILES['image']
            except:
                return ctypes.windll.user32.MessageBoxW(None, "에러", "사진을 첨부하세요", 5)
            blog.latitude = request.POST['latitude']
            blog.longtitude = request.POST['longtitude']
            blog.save()
            return redirect(index)
    else:
        return redirect(index)


def profile(request, user):
    blogs = Blog.objects.filter(user=request.user)
    profile = Profile.objects.get(user = request.user)
    context={
        "profile":profile,
        "blogs":blogs
        }   
    return render(request, 'profile.html', context)

def detail(request, post_id):
    post = Blog.objects.get(id=post_id)
    context = {
        "post":post
    }
    return render(request,'detail.html',context)