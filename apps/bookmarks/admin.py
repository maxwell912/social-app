from django.contrib import admin

from .models import BookmarkPost


@admin.register(BookmarkPost)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post'
    )
