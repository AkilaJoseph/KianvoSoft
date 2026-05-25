from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Service, BlogPost, Announcement


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'home', 'about', 'services', 'portfolio',
            'products', 'gallery', 'announcements',
            'testimonials', 'team', 'partners', 'contact', 'blog',
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/portfolio/{obj.slug}/'


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.published_date

    def location(self, obj):
        return f'/blog/{obj.slug}/'


class AnnouncementSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Announcement.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def location(self, obj):
        return f'/announcements/{obj.slug}/'


sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'services': ServiceSitemap,
    'blog': BlogSitemap,
    'announcements': AnnouncementSitemap,
}
