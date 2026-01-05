from django.contrib import admin
from .models import Category, Thread, Post, Reply, Vote, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "created_at")

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "creator", "pinned", "locked", "updated_at")
    list_filter = ("category", "pinned", "locked")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "author", "created_at")
    search_fields = ("content",)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "value", "created_at")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_moderator")
