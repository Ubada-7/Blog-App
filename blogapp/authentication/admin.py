from django.contrib import admin
from .models import BlogPost , Comment,Like,CommentReply,Moderator,Report
# Register your models here.


admin.site.register(Moderator)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Report)
admin.site.register(CommentReply)
@admin.register(BlogPost)
class post(admin.ModelAdmin):
    list_display = ('user','title','content','image','created_at')    