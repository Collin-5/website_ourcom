from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.StackedInline):
    model = Comment

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
CommentInline,
]

admin.site.register(Post, ArticleAdmin)
admin.site.register(Comment)
