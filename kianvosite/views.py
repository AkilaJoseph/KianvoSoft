from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    ProjectCategory, Project, Service, Testimonial,
    BlogCategory, BlogPost, ContactInquiry,
    NewsletterSubscriber, CompanyStat, Partner,
    RoadmapMilestone, TeamMember, ProductImage,
    GalleryCategory, GalleryImage, Announcement,
    AnnouncementApplication, HeroSlide, ActiveProduct
)
from .utils import send_contact_notification, send_application_notification


# Home Page
def home(request):
    context = {
        'featured_projects': Project.objects.filter(is_active=True, is_featured=True)[:6],
        'services': Service.objects.filter(is_active=True, service_type='current')[:4],
        'future_visions': Service.objects.filter(is_active=True, service_type='future')[:3],
        'roadmap_milestones': RoadmapMilestone.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True, is_featured=True)[:3],
        'blog_posts': BlogPost.objects.filter(is_published=True)[:3],
        'partners': Partner.objects.filter(is_active=True),
        'stats': CompanyStat.objects.filter(is_active=True),
        'team_members': TeamMember.objects.filter(is_active=True),
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'active_products': ActiveProduct.objects.filter(is_active=True),
    }
    return render(request, 'index.html', context)


# About Page
def about(request):
    context = {
        'stats': CompanyStat.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True)[:4],
        'team_members': TeamMember.objects.filter(is_active=True),
    }
    return render(request, 'about.html', context)


# Products Showcase Page (animated carousel, demo credentials)
def products(request):
    context = {
        'projects': Project.objects.filter(is_active=True),
        'categories': ProjectCategory.objects.filter(is_active=True),
        'featured_screenshots': ProductImage.objects.filter(is_featured=True)[:12],
    }
    return render(request, 'products.html', context)


# Testimonials Page
def testimonials(request):
    context = {
        'testimonials': Testimonial.objects.filter(is_active=True),
        'stats': CompanyStat.objects.filter(is_active=True),
    }
    return render(request, 'testimonials.html', context)


# Team Page
def team(request):
    context = {
        'team_members': TeamMember.objects.filter(is_active=True),
    }
    return render(request, 'team.html', context)


# Partners Page
def partners(request):
    context = {
        'partners': Partner.objects.filter(is_active=True),
    }
    return render(request, 'partners.html', context)


# Roadmap / Milestones Page
def roadmap(request):
    context = {
        'milestones': RoadmapMilestone.objects.filter(is_active=True),
    }
    return render(request, 'roadmap.html', context)


# Gallery Page (past classes, bootcamps, trainings)
def gallery(request):
    category_slug = request.GET.get('category', None)
    images = GalleryImage.objects.filter(is_active=True)
    categories = GalleryCategory.objects.filter(is_active=True)

    if category_slug:
        images = images.filter(category__slug=category_slug)

    context = {
        'images': images,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'gallery.html', context)


# Announcements Page
def announcements(request):
    context = {
        'announcements': Announcement.objects.filter(is_active=True, status__in=['open', 'closed']),
        'open_announcements': Announcement.objects.filter(is_active=True, status='open'),
    }
    return render(request, 'announcements.html', context)


# Announcement Detail + Application Form
def announcement_detail(request, slug):
    announcement = get_object_or_404(Announcement, slug=slug, is_active=True)
    already_applied = False

    if request.method == 'POST' and announcement.is_accepting_applications():
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        motivation = request.POST.get('motivation', '')

        if full_name and email and phone:
            # Check for duplicate
            if AnnouncementApplication.objects.filter(announcement=announcement, email=email).exists():
                already_applied = True
                messages.warning(request, 'You have already applied for this programme.')
            else:
                # Collect extra fields
                extra_data = {}
                if announcement.application_fields:
                    for line in announcement.application_fields.strip().split('\n'):
                        parts = line.split('|')
                        if len(parts) >= 2:
                            field_key = parts[0].strip().lower().replace(' ', '_')
                            field_value = request.POST.get(field_key, '')
                            if field_value:
                                extra_data[field_key] = field_value

                application = AnnouncementApplication.objects.create(
                    announcement=announcement,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    motivation=motivation,
                    extra_data=extra_data,
                )
                send_application_notification(application)
                messages.success(
                    request,
                    f'Your application for "{announcement.title}" has been submitted successfully! We will contact you at {email}.'
                )
                return redirect('announcement_detail', slug=slug)
        else:
            messages.error(request, 'Please fill in all required fields.')

    # Parse extra fields for the form
    extra_form_fields = []
    if announcement.application_fields:
        for line in announcement.application_fields.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                label = parts[0]
                field_type = parts[1]
                required = len(parts) >= 3 and parts[2].lower() == 'required'
                field_key = label.lower().replace(' ', '_')
                extra_form_fields.append({
                    'label': label,
                    'key': field_key,
                    'type': field_type,
                    'required': required,
                })

    context = {
        'announcement': announcement,
        'extra_fields': extra_form_fields,
        'already_applied': already_applied,
        'related_announcements': Announcement.objects.filter(
            is_active=True, announcement_type=announcement.announcement_type
        ).exclude(id=announcement.id)[:3],
    }
    return render(request, 'announcement_detail.html', context)


# Services Page
def services(request):
    context = {
        'current_services': Service.objects.filter(is_active=True, service_type='current'),
        'future_visions': Service.objects.filter(is_active=True, service_type='future'),
    }
    return render(request, 'service.html', context)


# Portfolio Page - Display all projects
def portfolio(request):
    category_slug = request.GET.get('category', None)

    projects = Project.objects.filter(is_active=True)
    categories = ProjectCategory.objects.filter(is_active=True)

    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category_slug,
        'stats': CompanyStat.objects.filter(is_active=True),
    }
    return render(request, 'portfolio.html', context)


# Project Detail Page
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    related_projects = Project.objects.filter(
        is_active=True,
        category=project.category
    ).exclude(id=project.id)[:3]

    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)


# Blog Page
def blog(request):
    category_slug = request.GET.get('category', None)

    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogCategory.objects.filter(is_active=True)

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    context = {
        'posts': posts,
        'categories': categories,
        'current_category': category_slug,
        'featured_posts': BlogPost.objects.filter(is_published=True, is_featured=True)[:3],
    }
    return render(request, 'blog.html', context)


# Blog Post Detail
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id)[:3]

    # Prev / Next navigation
    prev_post = BlogPost.objects.filter(
        is_published=True,
        published_date__lt=post.published_date
    ).order_by('-published_date').first()

    next_post = BlogPost.objects.filter(
        is_published=True,
        published_date__gt=post.published_date
    ).order_by('published_date').first()

    # Estimate reading time (avg 200 words/min)
    import re
    plain_text = re.sub(r'<[^>]+>', '', str(post.content))
    word_count = len(plain_text.split())
    reading_time = max(1, round(word_count / 200))

    context = {
        'post': post,
        'related_posts': related_posts,
        'prev_post': prev_post,
        'next_post': next_post,
        'reading_time': reading_time,
        'word_count': word_count,
    }
    return render(request, 'blog_detail.html', context)


# Contact Page
def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        service_type = request.POST.get('service', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        if name and email and message:
            inquiry = ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                service_type=service_type,
                subject=subject,
                message=message
            )
            send_contact_notification(inquiry)
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')

    context = {
        'services': Service.objects.filter(is_active=True),
    }
    return render(request, 'contact.html', context)


# Newsletter Subscription (AJAX)
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )

            if created:
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for subscribing to our newsletter!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'This email is already subscribed.'
                })

        return JsonResponse({
            'success': False,
            'message': 'Please provide a valid email address.'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Service Detail Page
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_projects = Project.objects.filter(is_active=True)[:4]

    context = {
        'service': service,
        'related_projects': related_projects,
    }
    return render(request, 'service_detail.html', context)
