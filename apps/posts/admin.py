from django.contrib import admin
from django_object_actions import DjangoObjectActions

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, DjangoObjectActions):
    list_display = (
        'user_id',
        'title',
        'created_at',
        'comment_allowed',
        'is_comment',
    )

    search_fields = ('title', 'created_at', )

    actions = ('block_comments', 'allow_comments',)
    change_actions = ('block_comments', 'allow_comments',)

    def allow_comments(self, request, queryset):
        """Unblock post commenting"""
        queryset.update(comment_allowed=True)

    def block_comments(self, request, queryset):
        """Block post commenting"""
        queryset.update(comment_allowed=False)
