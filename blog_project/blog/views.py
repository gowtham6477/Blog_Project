from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView

from .forms import CommentForm, PostForm
from .models import Post, Tag


def _published_posts():
	return (
		Post.objects.filter(status=Post.Status.PUBLISHED)
		.select_related("author")
		.prefetch_related("tags")
	)


def home(request):
	latest_posts = _published_posts().order_by("-published_at")[:5]
	popular_tags = (
		Tag.objects.annotate(
			post_count=Count("posts", filter=Q(posts__status=Post.Status.PUBLISHED))
		)
		.order_by("-post_count", "name")[:10]
	)
	return render(
		request,
		"blog/home.html",
		{
			"latest_posts": latest_posts,
			"popular_tags": popular_tags,
			"query": "",
		},
	)


def post_list(request):
	queryset = _published_posts()
	tag_slug = request.GET.get("tag")
	if tag_slug:
		queryset = queryset.filter(tags__slug=tag_slug)

	sort = request.GET.get("sort", "date")
	if sort == "views":
		queryset = queryset.order_by("-views_count", "-published_at")
	else:
		queryset = queryset.order_by("-published_at")

	paginator = Paginator(queryset, 8)
	page = request.GET.get("page")
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	popular_tags = (
		Tag.objects.annotate(
			post_count=Count("posts", filter=Q(posts__status=Post.Status.PUBLISHED))
		)
		.order_by("-post_count", "name")[:10]
	)

	return render(
		request,
		"blog/post_list.html",
		{
			"posts": posts,
			"popular_tags": popular_tags,
			"active_tag": tag_slug,
			"sort": sort,
		},
	)


def tag_posts(request, slug):
	queryset = _published_posts().filter(tags__slug=slug).order_by("-published_at")
	paginator = Paginator(queryset, 8)
	page = request.GET.get("page")
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	popular_tags = (
		Tag.objects.annotate(
			post_count=Count("posts", filter=Q(posts__status=Post.Status.PUBLISHED))
		)
		.order_by("-post_count", "name")[:10]
	)

	return render(
		request,
		"blog/post_list.html",
		{
			"posts": posts,
			"popular_tags": popular_tags,
			"active_tag": slug,
			"sort": "date",
		},
	)


def author_posts(request, username):
	queryset = _published_posts().filter(author__username=username).order_by("-published_at")
	paginator = Paginator(queryset, 8)
	page = request.GET.get("page")
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	popular_tags = (
		Tag.objects.annotate(
			post_count=Count("posts", filter=Q(posts__status=Post.Status.PUBLISHED))
		)
		.order_by("-post_count", "name")[:10]
	)

	return render(
		request,
		"blog/post_list.html",
		{
			"posts": posts,
			"popular_tags": popular_tags,
			"author_username": username,
			"sort": "date",
		},
	)


def search(request):
	query = request.GET.get("q", "").strip()
	queryset = _published_posts()
	if query:
		queryset = queryset.filter(Q(title__icontains=query) | Q(body__icontains=query))

	paginator = Paginator(queryset.order_by("-published_at"), 8)
	page = request.GET.get("page")
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	popular_tags = (
		Tag.objects.annotate(
			post_count=Count("posts", filter=Q(posts__status=Post.Status.PUBLISHED))
		)
		.order_by("-post_count", "name")[:10]
	)

	return render(
		request,
		"blog/post_list.html",
		{
			"posts": posts,
			"popular_tags": popular_tags,
			"query": query,
			"is_search": True,
		},
	)


def post_detail(request, slug):
	post = get_object_or_404(_published_posts(), slug=slug)
	Post.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
	post.refresh_from_db(fields=["views_count"])

	comments = post.comments.filter(approved=True)
	related_posts = (
		_published_posts()
		.filter(tags__in=post.tags.all())
		.exclude(pk=post.pk)
		.distinct()
		.order_by("-published_at")[:4]
	)

	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.created_at = timezone.now()
			comment.save()
			return redirect("blog:post_detail", slug=post.slug)
	else:
		form = CommentForm()

	return render(
		request,
		"blog/post_detail.html",
		{
			"post": post,
			"comments": comments,
			"form": form,
			"related_posts": related_posts,
		},
	)


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = "blog/post_form.html"

	def form_valid(self, form):
		post = form.save(commit=False)
		post.author = self.request.user
		if post.status == Post.Status.PUBLISHED and not post.published_at:
			post.published_at = timezone.now()
		post.save()
		form.save_m2m()
		return redirect(post.get_absolute_url())

	def get_success_url(self):
		return reverse("blog:post_list")
