from django.contrib import admin
from django.utils import timezone

from .models import Comment, Post, PostTag, Tag


class PostTagInline(admin.TabularInline):
	model = PostTag
	extra = 0
	autocomplete_fields = ["tag"]


@admin.action(description="Publish selected posts")
def publish_posts(modeladmin, request, queryset):
	queryset.update(status=Post.Status.PUBLISHED, published_at=timezone.now())


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "status", "published_at", "views_count")
	list_filter = ("status", "author", "published_at")
	search_fields = ("title", "body")
	prepopulated_fields = {"slug": ("title",)}
	date_hierarchy = "published_at"
	inlines = [PostTagInline]
	actions = [publish_posts]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}


@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
	queryset.update(approved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "post", "approved", "created_at")
	list_filter = ("approved", "created_at")
	search_fields = ("name", "email", "body")
	actions = [approve_comments]
