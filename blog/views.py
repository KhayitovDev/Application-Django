from typing import Any, Dict
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Comment, Category, ReplyToComment
from .forms import CommentForm, CustomUserCreationForm, PostCreateForm, CategoryCreateForm, CommentReplyForm


class UserLogin(LoginView):
    template_name='login.html'
    success_url=reverse_lazy('home_page')

class UserLogout(LogoutView):
    next_page=reverse_lazy('home_page')

class CreateUserView(CreateView):
    form_class=CustomUserCreationForm
    template_name='register.html'
    success_url=reverse_lazy('login')

class UsersListView(ListView):
    template_name='users.html'
    queryset=User.objects.all()

class PostListView(ListView):
    template_name = 'home_page.html'
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(Q(category__title__icontains=q)|Q(body__icontains=q))
        return queryset
    
class PostDetailView(DetailView):
    template_name='detail.html'
    queryset=Post.objects.all()
    context_object_name='detail_post'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        post=self.get_object()
        comment_queryset=Comment.objects.filter(post=post)
        context['comment_queryset']=comment_queryset
        return context
    
 
    def post(self, request, *args, **kwargs):
        post=self.get_object()
        user=request.user
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to like posts')
            return HttpResponseRedirect(reverse('login'))
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            messages.success(request, 'You have unliked the post')
        else:
            post.likes.add(request.user)
            messages.success(request, 'You have liked the post')
            
        return HttpResponseRedirect(reverse('detail', kwargs={'pk': post.pk}))

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create_new.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.object.status==Post.Status.PUBLISHED:
            return reverse_lazy('home_page')
        else:
            return reverse_lazy('draft_posts')
 
class PostUpdate(LoginRequiredMixin, UpdateView):
    model=Post
    form_class=PostCreateForm
    template_name='update.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response=super().form_valid(form)
        if self.object.status==Post.Status.PUBLISHED:
            messages.success(self.request, "Your post has been updated successfully!")
        else:
            messages.info(self.request, "Your post has been updated but still in Drafts")
        return response
    

    def get_success_url(self):
        post=get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.object.status==Post.Status.PUBLISHED:
            return reverse_lazy('detail', kwargs={'pk': post.pk})
        else:
            return reverse_lazy('draft_posts')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model=Post
    template_name='delete.html'
    success_url=reverse_lazy('home_page')
    context_object_name='obj'

class MostCommented(ListView):
    model=Post
    template_name='most_commented.html'
    context_object_name='posts'

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset=queryset.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]
        return queryset
    
class MostLiked(ListView):
    model=Post
    template_name='most_liked.html'
    context_object_name='posts'

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset=queryset.annotate(likes_count=Count('likes', distinct=True)).order_by('-likes_count')
        return queryset

class DraftPostsListView(LoginRequiredMixin, ListView):
    template_name='draft_list.html'
    model=Post
    context_object_name='draft_posts'
    paginate_by=3

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, status=Post.Status.DRAFT)


class DraftPostDetailView(DetailView):
    model=Post
    template_name='draft_detail.html'
    context_object_name='draft_detail_post'

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset=queryset.filter(author=self.request.user, status=Post.Status.DRAFT)
        return queryset
    

class CategoryCreateView(CreateView):
    form_class=CategoryCreateForm
    template_name='post_create_new.html'
    success_url=reverse_lazy('category')

class CategoryListView(ListView):
    template_name='category_list.html'
    queryset=Category.objects.all()
    context_object_name='categories'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment.html'

    def form_valid(self, form):
        form.instance.name_id = self.request.user.id
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse_lazy('detail', kwargs={'pk': post_id})

class CommentListView(ListView):
    context_object_name='comments'
    template_name='comments.html'

    def get_queryset(self):
        pk=self.kwargs['pk']
        queryset=Comment.objects.filter(post__id=pk)
        return queryset
    
class CommentReplyView(LoginRequiredMixin, CreateView):
    model=ReplyToComment
    form_class = CommentReplyForm
    template_name = 'reply.html'

    def form_valid(self, form):
        replied_to_comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        form.instance.replied_to_comment = replied_to_comment
        form.instance.replied_to = self.request.user
        return super().form_valid(form)
    

    def get_success_url(self) -> str:
        comment_id=self.kwargs['pk']
        return reverse_lazy('comment_detail', kwargs={'pk':comment_id})
 
class CommentUpdate(UpdateView):
    model=Comment
    form_class=CommentForm
    template_name='update.html'
    

    def get_success_url(self) -> str:
        pk=self.object.post.pk
        return reverse_lazy('comments', kwargs={'pk':pk})

 



        

