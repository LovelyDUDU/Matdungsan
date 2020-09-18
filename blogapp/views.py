from django.shortcuts import render,redirect, get_object_or_404
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
            blogs = Blog.objects.all()
            return render(request, 'create.html', {'blogs': blogs})
    
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
            return redirect(create)
    else:
        return redirect(create)


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

def update_profile(request, user):
    if request.method=="GET":
        profile = Profile.objects.get(user = request.user)
        context={
            "profile" : profile
        }
        return render(request, "update_profile.html", context)
    elif request.method=="POST":
        profile = Profile.objects.get(user=request.user)
        profile.nickname=request.POST['nickname']
        profile.name=request.POST['name']
        profile.gender = request.POST['gender']
        profile.birth=request.POST['birth']
        try:
            profile.imgae = request.FILES['image']
        except:
            pass
        profile.save()
        return redirect('/' + 'blogapp/profile/' + user)