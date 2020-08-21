from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Blog

def index(request):
    blogs = Blog.objects
    return render(request, 'index.html', {'blogs': blogs})


def create(request):
    if request.method == "GET":
        return render(request, 'index.html')
    
    elif request.method =="POST":
        blog = Blog()
        blog.user = request.user
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.pub_date = timezone.datetime.now()
        try:
            blog.image=request.FILES['image']
        except:
            pass
        blog.latitude = request.POST['latitude']
        blog.longtitude = request.POST['longtitude']
        public = request.POST.get('public',False)  
        if public == "1":
            blog.public = True
        blog.save()
        return redirect(index)
    