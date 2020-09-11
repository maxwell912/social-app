from django.contrib import admin

from .models import Reaction


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    search_fields = (
        'post',
        'description',
    )
    list_display = (
        'id',
        'post',
        'description',
    )
