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
	list_display = (
		"title",
		"author",
		"status",
		"published_at",
		"views_count",
		"tag_list",
	)
	list_filter = ("status", "author", "published_at")
	search_fields = ("title", "body")
	prepopulated_fields = {"slug": ("title",)}
	date_hierarchy = "published_at"
	inlines = [PostTagInline]
	actions = [publish_posts]

	def tag_list(self, obj):
		return ", ".join(tag.name for tag in obj.tags.all())

	tag_list.short_description = "Tags"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("name", "slug", "description")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}


@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
	queryset.update(approved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("post", "author_name", "is_approved", "created_at")
	list_filter = ("approved", "created_at")
	search_fields = ("name", "email", "body")
	actions = [approve_comments]

	def author_name(self, obj):
		return obj.author_name

	def is_approved(self, obj):
		return obj.is_approved

	author_name.short_description = "Author name"
	is_approved.short_description = "Approved"
