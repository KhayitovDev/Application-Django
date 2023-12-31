from django.contrib import admin
from .models import Post, Category, Comment, ReplyToComment
# Register your models here.

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ReplyToComment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title', 'slug', 'author', 'published_at', 'status']
    list_filter = ['status', 'created_at', 'published_at', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    ordering = ['status', 'published_at']