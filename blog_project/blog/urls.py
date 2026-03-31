from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
	path("", views.home, name="home"),
	path("posts/", views.post_list, name="post_list"),
	path("search/", views.search, name="search"),
	path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
]
