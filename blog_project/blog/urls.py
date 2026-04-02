from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
	path("", views.home, name="home"),
	path("posts/", views.post_list, name="post_list"),
	path("search/", views.search, name="search"),
	path("tag/<slug:slug>/", views.tag_posts, name="tag_posts"),
	path("tags/<slug:slug>/", views.tag_posts, name="tag_posts_alt"),
	path("author/<str:username>/", views.author_posts, name="author_posts"),
	path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
	path("posts/new/", views.PostCreateView.as_view(), name="post_create"),
	path("rss/", LatestPostsFeed(), name="rss_feed"),
]
