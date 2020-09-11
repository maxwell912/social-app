from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    search_fields = ('post',)
    list_display = (
        'id',
        'post',
    )
