from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()
    # def __str__(self):
    #     return self.name
    
class Comment(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.post.title}" 