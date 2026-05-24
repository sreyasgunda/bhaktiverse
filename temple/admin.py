from django.contrib import admin
from .models import Temple


@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
