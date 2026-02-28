from django.db import models
from django.utils import timezone

# Project Category Model
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(max_length=100, help_text="FontAwesome or Flaticon class (e.g., 'flaticon-software-development')")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


# Project/System Model
class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
        ('maintenance', 'Under Maintenance'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, help_text="Short description/tagline")
    description = models.TextField()
    full_description = models.TextField(blank=True, help_text="Detailed description for project detail page")

    # Categorization
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')

    # Technical Details
    technologies = models.CharField(max_length=500, help_text="Comma-separated list of technologies used")
    features = models.TextField(blank=True, help_text="Key features (one per line)")

    # Media
    icon_class = models.CharField(max_length=100, default='flaticon-software-development', help_text="Icon class for display")
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='projects/banners/', blank=True, null=True)
    screenshot_1 = models.ImageField(upload_to='projects/screenshots/', blank=True, null=True)
    screenshot_2 = models.ImageField(upload_to='projects/screenshots/', blank=True, null=True)
    screenshot_3 = models.ImageField(upload_to='projects/screenshots/', blank=True, null=True)

    # Status & Links
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    demo_url = models.URLField(blank=True, null=True, help_text="Live demo link")
    documentation_url = models.URLField(blank=True, null=True)

    # Display Options
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    # Timestamps
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return self.name

    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def get_technologies_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [t.strip() for t in self.technologies.split(',') if t.strip()]
        return []


# Service Model
class Service(models.Model):
    SERVICE_TYPES = [
        ('current', 'Current Service'),
        ('future', 'Future Vision (Planned)'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='current', help_text="Is this a current service or a future planned vision?")
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default='flaticon-software-development')

    # Specific to Future Vision
    timeline_text = models.CharField(max_length=100, blank=True, help_text="E.g., '2026-2027' (only used for future vision services)")

    # Features for this service
    features = models.TextField(blank=True, help_text="Key features (one per line)")
    technologies = models.CharField(max_length=500, blank=True, help_text="Technologies used for this service")

    # Media
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    # Display Options
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []


# Testimonial Model
class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    content = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


# Blog Category
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, default='flaticon-web-research')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# Blog Post Model
class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=500, help_text="Short summary for listing pages")
    content = models.TextField()

    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.CharField(max_length=200, default='KianvoSoft')

    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title


# Contact Inquiry Model
class ContactInquiry(models.Model):
    SERVICE_CHOICES = [
        ('software', 'Custom Software Development'),
        ('web', 'Web Application Development'),
        ('mobile', 'Mobile App Development'),
        ('ai', 'AI & Machine Learning'),
        ('automation', 'Automation Systems'),
        ('analytics', 'Data Analytics'),
        ('consulting', 'IT Consulting'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True)
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True, help_text="Internal notes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or self.service_type}"


# Newsletter Subscriber Model
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


# Company Statistics Model (for dynamic counters)
class CompanyStat(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., 'Projects Completed'")
    value = models.IntegerField()
    suffix = models.CharField(max_length=10, default='+', help_text="e.g., '+', '%', 'K'")
    icon_class = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Company Statistics"
        ordering = ['order']

    def __str__(self):
        return f"{self.name}: {self.value}{self.suffix}"


# Partner/Client Logo Model
class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


# Roadmap / Timeline Milestone Model
class RoadmapMilestone(models.Model):
    year = models.CharField(max_length=50, help_text="E.g., '2025' or 'Q3 2026'")
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year} - {self.title}"
