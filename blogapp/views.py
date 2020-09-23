from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone
from .models import Blog, Profile, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
import json
import ctypes

def index(request):
    blogs = Blog.objects.all()
    temp = Blog.objects.filter(tags__name__in=["저거"])
    print(blogs)
    for i in temp:
        print(i.title)
        print(i.content)
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
            blog.image=request.FILES['image']
            blog.latitude = request.POST['latitude']
            blog.longtitude = request.POST['longtitude']
            tags=request.POST.get('tags', '').split(',')
            blog.save()
            for tag in tags:
                tag = tag.strip()
                blog.tags.add(tag)
            return redirect(create)
    else:
        return redirect(create)

def detail(request, post_id):
    post = Blog.objects.get(id=post_id)
    comment = Comment.objects.filter(post=post.id)
    context = {
        "post":post,
        "comment": comment
    }
    return render(request,'detail.html',context)

def likes(request):
    if request.is_ajax():
        post_id = request.GET['post_id']
        post = Blog.objects.get(id=post_id)

        if not request.user.is_authenticated:
            message = "로그인이 필요합니다."
            context ={'like_count' : post.like.count(), "message":message}
            return HttpResponse(json.dumps(context), content_type = 'application/json')
        
        user = request.user
        if post.like.filter(id = user.id).exists():
            post.like.remove(user)
            message = "좋아요 취소"
        else:
            post.like.add(user)
            message = "좋아요"
        
        context={'like_count' : post.like.count(), "message": message}
        return HttpResponse(json.dumps(context), content_type='application/json')

def create_comment(request, post_id):
    if request.method =="POST":
        comment = Comment()
        comment.user = request.user
        comment.post = Blog.objects.get(id=post_id)
        comment.content = request.POST['comment']
        comment.created_at = timezone.datetime.now()
        comment.save()
        return redirect('/blogapp/detail/' + str(post_id))

def delete_comment(request, post_id, comment_id):
    d_comment = Comment.objects.get(id=comment_id)
    d_comment.delete()
    return redirect('/blogapp/detail/' + str(post_id))

def profile(request, user):
    user =User.objects.get(id=request.user.id)
    blogs = Blog.objects.filter(user =request.user).order_by('-id')
    paginator=Paginator(blogs,9) #blogs 객체를 9개 단위로 자름
    page = request.GET.get('page')
    posts=paginator.get_page(page)
    profile = Profile.objects.get(user = request.user)
    post_likes = user.likes.all()
    context={
        "profile":profile,
        "blogs":blogs,
        "post_likes" : post_likes,
        "posts":posts,
        }   
    return render(request, 'profile.html', context)


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
            profile.image = request.FILES['image']
        except:
            pass
        profile.save()
        return redirect('/' + 'blogapp/profile/' + user)