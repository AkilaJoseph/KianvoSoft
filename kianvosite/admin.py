from django.contrib import admin
from django.utils.html import format_html
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import (
    ProjectCategory, Project, Service, Testimonial,
    BlogCategory, BlogPost, ContactInquiry,
    NewsletterSubscriber, CompanyStat, Partner,
    TeamMember, ProductImage, SocialLink,
    GalleryCategory, GalleryImage, Announcement,
    AnnouncementApplication, HeroSlide, ActiveProduct
)


CONTENT_WRITING_GUIDE = """
<div style="background:#f0f7ff;border-left:4px solid #1a73e8;padding:14px 18px;margin-bottom:12px;border-radius:0 8px 8px 0;font-size:13px;line-height:1.7;">
  <strong style="color:#1a73e8;">&#128221; Content Writing Guide — Article Structure</strong><br>
  Use the <strong>Format</strong> dropdown in the editor to structure your article:<br>
  &bull; <strong>Section Heading (H2)</strong> — main sections (these become TOC entries + auto-numbered)<br>
  &bull; <strong>Sub-heading (H3)</strong> — sub-sections inside an H2<br>
  &bull; <strong>Minor Heading (H4)</strong> — minor emphasis headings<br>
  &bull; <strong>Paragraph</strong> — regular body text<br>
  &bull; <strong>Code Block (pre)</strong> — code snippets<br>
  Use <strong>Numbered List</strong> / <strong>Bullet List</strong> for lists &nbsp;|&nbsp;
  <strong>Table</strong> for comparison tables &nbsp;|&nbsp;
  <strong>Blockquote</strong> for pull quotes.
</div>
"""


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorUploadingWidget(config_name='blog'),
        help_text=CONTENT_WRITING_GUIDE,
    )

    class Meta:
        model = BlogPost
        fields = '__all__'


# Customize Admin Site Header
admin.site.site_header = "KianvoSoft Admin"
admin.site.site_title = "KianvoSoft Admin Portal"
admin.site.index_title = "Welcome to KianvoSoft Administration"


# Project Category Admin
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon_class', 'order', 'is_active', 'project_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']

    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


# Inline for Product Screenshots
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'caption', 'is_featured', 'order']
    ordering = ['-is_featured', 'order']


# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'category', 'status', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'is_active']
    search_fields = ['name', 'tagline', 'description', 'technologies']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active', 'order', 'status']
    date_hierarchy = 'created_at'
    ordering = ['-is_featured', 'order', '-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'tagline', 'description', 'full_description')
        }),
        ('Categorization & Technical', {
            'fields': ('category', 'technologies', 'features', 'icon_class')
        }),
        ('Media', {
            'fields': ('thumbnail', 'banner_image', 'screenshot_1', 'screenshot_2', 'screenshot_3'),
            'classes': ('collapse',)
        }),
        ('Demo Credentials', {
            'fields': ('demo_url', 'demo_username', 'demo_password'),
            'classes': ('collapse',),
            'description': 'Provide demo credentials so users can test the product live.',
        }),
        ('Status & Links', {
            'fields': ('status', 'documentation_url', 'completed_date')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


# Service Admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'is_featured', 'is_active', 'order']
    list_filter = ['service_type', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'technologies']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['order', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'service_type', 'timeline_text', 'short_description', 'description', 'icon_class')
        }),
        ('Details', {
            'fields': ('features', 'technologies', 'image')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


# Testimonial Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'project', 'is_featured', 'is_active']
    list_filter = ['rating', 'is_featured', 'is_active', 'project']
    search_fields = ['client_name', 'client_company', 'content']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-is_featured', 'order', '-created_at']


# Blog Category Admin
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'post_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


# Blog Post Admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'category', 'author', 'is_featured', 'is_published', 'published_date', 'preview_link']
    list_filter = ['category', 'is_featured', 'is_published', 'published_date']
    search_fields = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    fieldsets = (
        ('Article Details', {
            'fields': ('title', 'slug', 'excerpt', 'featured_image'),
            'description': 'The title auto-populates the slug. The excerpt is the short summary shown on the blog listing page.',
        }),
        ('Article Content', {
            'fields': ('content',),
            'description': 'Use the Format dropdown to structure your article with H2/H3 headings — these auto-generate the Table of Contents on the front end.',
        }),
        ('Classification & Publishing', {
            'fields': ('category', 'author', 'published_date', 'is_featured', 'is_published'),
        }),
    )

    def preview_link(self, obj):
        if obj.slug and obj.is_published:
            url = f'/blog/{obj.slug}/'
            return format_html(
                '<a href="{}" target="_blank" style="color:#1a73e8;font-weight:600;">&#128279; View</a>', url
            )
        return '—'
    preview_link.short_description = 'Preview'


# Contact Inquiry Admin
@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_type', 'status', 'created_at', 'status_badge']
    list_filter = ['status', 'service_type', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('service_type', 'subject', 'message')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'new': '#dc3545',
            'in_progress': '#ffc107',
            'responded': '#17a2b8',
            'closed': '#28a745',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


# Newsletter Subscriber Admin
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
    date_hierarchy = 'subscribed_at'
    ordering = ['-subscribed_at']


# Company Stats Admin
@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'suffix', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['value', 'suffix', 'order', 'is_active']
    ordering = ['order']


# Partner Admin
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'website_url', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 40px;"/>', obj.logo.url)
        return "No logo"
    logo_preview.short_description = 'Logo'




# Team Member Admin
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'image_preview', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'role', 'bio']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 40px; width: 40px; object-fit: cover; border-radius: 50%;"/>', obj.image.url)
        return format_html('<span style="color:#6c757d;">No image</span>')
    image_preview.short_description = 'Photo'


# Gallery Category Admin
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'image_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


# Gallery Image Admin
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'is_featured', 'is_active', 'order', 'image_preview']
    list_filter = ['category', 'is_featured', 'is_active', 'event_date']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['-is_featured', 'order', '-event_date']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 60px; object-fit: cover; border-radius: 4px;"/>', obj.image.url)
        return '—'
    image_preview.short_description = 'Preview'


# Announcement Admin
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'status', 'start_date', 'application_deadline', 'applications_count', 'is_featured']
    list_filter = ['announcement_type', 'status', 'is_featured', 'is_active']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'start_date'
    ordering = ['-is_featured', 'order', '-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'announcement_type', 'short_description', 'description', 'cover_image')
        }),
        ('Logistics', {
            'fields': ('start_date', 'end_date', 'application_deadline', 'venue', 'mode', 'fee')
        }),
        ('Capacity & Requirements', {
            'fields': ('capacity', 'prerequisites'),
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone'),
        }),
        ('Applications', {
            'fields': ('collect_applications', 'application_fields'),
            'description': 'Extra fields for the application form. Default fields (name, email, phone, motivation) are always included.',
        }),
        ('Display', {
            'fields': ('status', 'is_featured', 'is_active', 'order'),
        }),
    )

    def applications_count(self, obj):
        return obj.applications.count()
    applications_count.short_description = 'Apps'


# Announcement Application Admin
@admin.register(AnnouncementApplication)
class AnnouncementApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'announcement', 'status', 'applied_at']
    list_filter = ['status', 'announcement']
    search_fields = ['full_name', 'email', 'phone']
    list_editable = ['status']
    date_hierarchy = 'applied_at'
    ordering = ['-applied_at']
    readonly_fields = ['applied_at', 'updated_at']

    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Application', {
            'fields': ('motivation', 'extra_data', 'announcement')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Social Link Admin
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'icon_class', 'url', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['platform', 'url']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'platform']


# Hero Slide Admin
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['order']


# Active Product Admin
@admin.register(ActiveProduct)
class ActiveProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'project_link', 'is_featured', 'is_active', 'order']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['name', 'short_description']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['category', 'order']

    def project_link(self, obj):
        if obj.project:
            url = f'/portfolio/{obj.project.slug}/'
            from django.utils.html import format_html
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.project.name)
        return '—'
    project_link.short_description = 'Linked Project'
