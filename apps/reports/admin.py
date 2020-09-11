from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'post_id',
        'reason',
        'created_at',
    )

    autocomplete_fields = (
        'user_id',
        'post_id',
    )
