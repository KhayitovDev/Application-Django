from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post, Category, ReplyToComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model=ReplyToComment
        fields=['body']      


class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['category', 'title', 'body', 'status' ]

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['title']


class CustomUserCreationForm(UserCreationForm):

  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None
