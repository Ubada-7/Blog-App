from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    liked= models.ManyToManyField(User, related_name='mancb', blank=True)
    approved = models.BooleanField(default=False)
    reports = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_comments')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class CommentReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()
    parent_reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_replies')

    def __str__(self):
        return f"Reply by {self.user.username} on {self.comment}"

from django.db import models
from django.contrib.auth.models import User # Import the BlogPost model from your app

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    def __str__(self):
        return f"{self.user.username} liked a post"


from django.contrib.auth.models import User
from django.db import models

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


def make_user_moderator(user):
    if not Moderator.objects.exists():
        moderator = Moderator.objects.create(user=user)
from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for '{self.post.title}' by {self.user.username}"
