from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=60, unique=True, db_index=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class Post(models.Model):
	class Status(models.TextChoices):
		DRAFT = "draft", "Draft"
		PUBLISHED = "published", "Published"

	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, db_index=True)
	body = models.TextField()
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
	)
	status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	published_at = models.DateTimeField(null=True, blank=True, db_index=True)
	cover_image = models.ImageField(upload_to="covers/", blank=True)
	views_count = models.PositiveIntegerField(default=0)
	tags = models.ManyToManyField("Tag", through="PostTag", related_name="posts")

	class Meta:
		ordering = ["-published_at", "-created_at"]
		indexes = [
			models.Index(fields=["slug"]),
			models.Index(fields=["status", "published_at"]),
			models.Index(fields=["author", "status"]),
		]

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.title) or "post"
			candidate = base_slug
			counter = 1
			while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
				counter += 1
				candidate = f"{base_slug}-{counter}"
			self.slug = candidate
		super().save(*args, **kwargs)


class PostTag(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("post", "tag")
		indexes = [models.Index(fields=["post", "tag"])]

	def __str__(self) -> str:
		return f"{self.post} · {self.tag}"


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	name = models.CharField(max_length=100)
	email = models.EmailField()
	body = models.TextField()
	approved = models.BooleanField(default=False, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
		indexes = [
			models.Index(fields=["post", "approved", "created_at"]),
		]

	def __str__(self) -> str:
		return f"Comment by {self.name}"
