from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created')
    list_filter = ('author', 'created', 'created')
    search_field = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('by', 'content', 'approved')


admin.site.register(Comment, CommentAdmin)