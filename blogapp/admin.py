from django.contrib import admin
from .models import Blog, Profile, Comment,FollowRelation, Board, Board_Comment
# Register your models here.

admin.site.register(Board)
admin.site.register(Blog)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(FollowRelation)
admin.site.register(Board_Comment)