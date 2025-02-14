from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    actions = ["publish_recipes"]

    def publish_recipes(self, request, queryset):
        queryset.update(status="published")
    publish_recipes.short_description = "Mark selected recipes as published"