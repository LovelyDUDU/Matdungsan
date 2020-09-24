from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone
from .models import Blog, Profile, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
import json
import ctypes

def search_mountain(request):
    schText=request.GET['search']
    mountains = Mountain.objects.filter(name__icontains=schText)
    return render(request, 'search_mountain.html', {'mountains':mountains})


def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs})

def tag_search(request):
    schTag = request.GET['tag_search']
    blogs = Blog.objects.all()
    tags = Blog.objects.filter(tags__name__in=[schTag])
    for i in tags:
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
    who_like = post.like.all() #좋아요 누른 사람
    for i in who_like:
        p = Profile.objects.get(user=i)
        print(i.username + " - " + p.nickname + " - " + p.name)
    return render(request,'detail.html',context)

def likes(request):
    if request.is_ajax():
        post_id = request.GET['post_id']
        post = Blog.objects.get(id=post_id)

        if not request.user.is_authenticated:
            message = "로그인이 필요합니다."
            context ={'like_count' : post.like.count(), "message":message}
            return HttpResponse(json.dumps(context), content_type = 'application/json')
        print(post)
        user = request.user
        if post.like.filter(id = user.id).exists():
            post.like.remove(user)
            message = "좋아요 취소"
        else:
            post.like.add(user)
            message = "좋아요"
        
        context={'like_count' : post.like.count(), "message": message}
        
        return HttpResponse(json.dumps(context), content_type='application/json')

def follow(request):
    if request.is_ajax():
        profile_id = request.GET['profile_id']
        p_user = Profile.objects.get(id=profile_id) #프로필주인
        q_user = Profile.objects.get(id=request.user.id) #나
        print("접속자 : " + str(q_user))
        print("프로필주인 : " + str(p_user))
        if not request.user.is_authenticated:
            message = "로그인이 필요합니다."
            context ={
                'following_count' : p_user.following.count(),
                'follower_count' : p_user.follower.count(),
                 "message":message,
                 }
            return HttpResponse(json.dumps(context), content_type = 'application/json')
        if p_user.follower.filter(id = q_user.id).exists(): #프로필주인 follower에 내가 있으면 팔로우 취소 
            p_user.follower.remove(q_user.id) # 프로필주인 follower 제거, 
            #q_user.following.remove(p_user.id) # 나의 following 제거
            message = "팔로우 취소"
            print("팔로우 취소")
        else: #프로필주인 follower에 내가 없으면 q_user -> p_user
            p_user.follower.add(q_user.id) #프로필주인의 팔로워에 나를 넣고
            #q_user.following.add(p_user.id) #나의 팔로잉에 상대를 넣고
            message = "팔로우"
            print("팔로우")
        
        context={
            'following_count' : p_user.following.count(),
            'follower_count' : p_user.follower.count(),
            "message": message,
            }
        
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
    user =User.objects.get(username=user)
    blogs = Blog.objects.filter(user =user).order_by('-id')
    paginator=Paginator(blogs,9) #blogs 객체를 9개 단위로 자름
    page = request.GET.get('page')
    posts=paginator.get_page(page)
    profile = Profile.objects.get(user = user)
    post_likes = user.likes.all()
    # print(profile)
    # print(user)
    context={
        "profile":profile,
        "blogs":blogs,
        "post_likes" : post_likes,
        "posts":posts,
        }
    # print("좋아요한 게시물 출력")
    # for i in post_likes:
    #     print(i.title + " - " + i.content)
    return render(request, 'profile.html', context)

def p_profile(request, post_id):
    post = Blog.objects.get(id=post_id)
    user = User.objects.get(post=post)
    profile = Profile.objects.get(user= user)
    context ={
        "profile" : profile,
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
        profile.age_group=request.POST['age_group']
        try:
            profile.image = request.FILES['image']
        except:
            pass
        profile.save()
        return redirect('/' + 'blogapp/profile/' + user)