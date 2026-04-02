from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())

    def lastmod(self, obj):
        return obj.updated_at
