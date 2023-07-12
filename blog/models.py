from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    title=models.CharField(max_length=250)

    def __str__(self):
        return self.title
    


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT='DF', 'Draft'
        PUBLISHED='PB', 'Published'
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True )
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250)
    body=models.TextField()
    published_at=models.DateTimeField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    likes=models.ManyToManyField(User, related_name='post_likes')

    def like_count(self):
        return self.likes.count()


    class Meta:
        ordering=['-published_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes=[models.Index(fields=['-published_at'])]

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField()
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
  

    class  Meta:
        ordering=['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by{self.name} on {self.post}"
    

class ReplyToComment(models.Model):
    replied_to=models.ForeignKey(User, on_delete=models.CASCADE)
    replied_to_comment=models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.replied_to_comment} by {self.replied_to}"
    
