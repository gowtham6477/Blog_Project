from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Post


class LatestPostsFeed(Feed):
    title = "DevJournal"
    link = "/rss/"
    description = "Latest published posts from DevJournal."

    def items(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())
            .order_by("-published_at")[:20]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()
