from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import (
    ProjectCategory, Project, Service, Testimonial,
    BlogCategory, BlogPost, ContactInquiry,
    NewsletterSubscriber, CompanyStat, Partner
)


# Home Page
def home(request):
    context = {
        'featured_projects': Project.objects.filter(is_active=True, is_featured=True)[:6],
        'services': Service.objects.filter(is_active=True)[:6],
        'testimonials': Testimonial.objects.filter(is_active=True, is_featured=True)[:3],
        'blog_posts': BlogPost.objects.filter(is_published=True)[:3],
        'partners': Partner.objects.filter(is_active=True),
        'stats': CompanyStat.objects.filter(is_active=True),
    }
    return render(request, 'index.html', context)


# About Page
def about(request):
    context = {
        'stats': CompanyStat.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True)[:4],
    }
    return render(request, 'about.html', context)


# Services Page
def services(request):
    context = {
        'services': Service.objects.filter(is_active=True),
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

    context = {
        'post': post,
        'related_posts': related_posts,
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
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                service_type=service_type,
                subject=subject,
                message=message
            )
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
