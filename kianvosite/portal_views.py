from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils.html import format_html, mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import (
    Project, ProjectCategory, Service, Testimonial,
    BlogPost, BlogCategory, ContactInquiry, NewsletterSubscriber,
    CompanyStat, Partner, TeamMember, Announcement,
    AnnouncementApplication, GalleryImage, GalleryCategory,
    RoadmapMilestone, ProductImage, SocialLink
)

# ---------------------------------------------------------------------------
#  Icon picker
# ---------------------------------------------------------------------------

ICON_CHOICES = [
    # ── Flaticon (Bantec theme) ──
    ('flaticon-software-development', 'Software Development'),
    ('flaticon-web-research', 'Web Research'),
    ('flaticon-data-scientist', 'Data Scientist'),
    ('flaticon-consultant', 'Consultant'),
    ('flaticon-satellite-signal', 'Satellite / Connectivity'),
    ('flaticon-cyber-security', 'Cyber Security'),
    ('flaticon-database', 'Database'),
    ('flaticon-cloud-computing', 'Cloud Computing'),
    ('flaticon-cloud-storage', 'Cloud Storage'),
    ('flaticon-mobile-phone-1', 'Mobile Phone'),
    ('flaticon-mobile-app', 'Mobile App'),
    ('flaticon-mobile-data', 'Mobile Data'),
    ('flaticon-iphone-1', 'iPhone'),
    ('flaticon-laptop-1', 'Laptop'),
    ('flaticon-imac-computer', 'iMac / Desktop'),
    ('flaticon-computer-mouse', 'Computer Mouse'),
    ('flaticon-global-network', 'Global Network'),
    ('flaticon-radio-tower', 'Radio Tower'),
    ('flaticon-it', 'IT Service'),
    ('flaticon-it-service', 'IT Service Alt'),
    ('flaticon-machine-repair', 'Machine Repair'),
    ('flaticon-rocket', 'Rocket / Launch'),
    ('flaticon-eye', 'Eye / Vision'),
    ('flaticon-idea', 'Idea / Innovation'),
    ('flaticon-good-feedback', 'Good Feedback'),
    ('flaticon-telephone-call', 'Telephone Call'),
    ('flaticon-phone-call', 'Phone Call'),
    ('flaticon-phone-call-1', 'Phone Call Alt'),
    ('flaticon-email', 'Email'),
    ('flaticon-mail', 'Mail'),
    ('flaticon-location', 'Location'),
    ('flaticon-clock', 'Clock'),
    ('flaticon-loupe', 'Search / Loupe'),
    ('flaticon-incoming-message', 'Incoming Message'),
    ('flaticon-twitter', 'Twitter'),
    ('flaticon-instagram', 'Instagram'),
    # ── Font Awesome Solid ──
    ('fas fa-code', 'Code (FA)'),
    ('fas fa-laptop-code', 'Laptop Code (FA)'),
    ('fas fa-server', 'Server (FA)'),
    ('fas fa-cogs', 'Cogs (FA)'),
    ('fas fa-cog', 'Cog (FA)'),
    ('fas fa-cloud', 'Cloud (FA)'),
    ('fas fa-database', 'Database (FA)'),
    ('fas fa-shield-alt', 'Shield (FA)'),
    ('fas fa-mobile-alt', 'Mobile (FA)'),
    ('fas fa-tablet-alt', 'Tablet (FA)'),
    ('fas fa-chart-line', 'Chart Line (FA)'),
    ('fas fa-chart-bar', 'Chart Bar (FA)'),
    ('fas fa-user-graduate', 'Graduate (FA)'),
    ('fas fa-chalkboard-teacher', 'Teacher (FA)'),
    ('fas fa-hands-helping', 'Helping Hands (FA)'),
    ('fas fa-rocket', 'Rocket (FA)'),
    ('fas fa-lightbulb', 'Lightbulb (FA)'),
    ('fas fa-globe', 'Globe (FA)'),
    ('fas fa-wifi', 'WiFi (FA)'),
    ('fas fa-brain', 'Brain (FA)'),
    ('fas fa-robot', 'Robot (FA)'),
    ('fas fa-network-wired', 'Network (FA)'),
    ('fas fa-paint-brush', 'Design (FA)'),
    ('fas fa-layer-group', 'Layers (FA)'),
]

class IconPickerWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        value = value or ''
        input_id = attrs.get('id', name) if attrs else name
        icon_blocks = []
        for icon_class, label in ICON_CHOICES:
            sel = ' ks-icon-sel' if icon_class == value else ''
            icon_blocks.append(
                '<div class="ks-icon-opt%s" data-val="%s" title="%s">'
                '<i class="%s"></i></div>' % (sel, icon_class, label, icon_class)
            )
        hidden = '<input type="hidden" name="%s" id="%s" value="%s">' % (name, input_id, value)
        grid = '<div class="ks-icon-grid" data-target="%s">%s</div>' % (input_id, ''.join(icon_blocks))
        script = (
            '<script>'
            '(function(){'
            'var g=document.querySelector(\'.ks-icon-grid[data-target="%s"]\');'
            'if(!g)return;'
            'g.addEventListener("click",function(e){'
            'var o=e.target.closest(".ks-icon-opt");'
            'if(!o)return;'
            'g.querySelectorAll(".ks-icon-opt").forEach(function(x){x.classList.remove("ks-icon-sel");});'
            'o.classList.add("ks-icon-sel");'
            'document.getElementById("%s").value=o.getAttribute("data-val");'
            '});'
            '})();'
            '</script>'
        ) % (input_id, input_id)
        return mark_safe(hidden + grid + script)

# ---------------------------------------------------------------------------
#  Auth
# ---------------------------------------------------------------------------

def portal_login(request):
    if request.user.is_authenticated:
        return redirect('portal_dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username',''), password=request.POST.get('password',''))
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('portal_dashboard')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'portal/login.html')

def portal_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('portal_login')

# ---------------------------------------------------------------------------
#  Dashboard
# ---------------------------------------------------------------------------

def _stats():
    return {
        'total_projects': Project.objects.filter(is_active=True).count(),
        'total_product_images': ProductImage.objects.count(),
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_blog_posts': BlogPost.objects.filter(is_published=True).count(),
        'total_inquiries': ContactInquiry.objects.count(),
        'pending_inquiries': ContactInquiry.objects.filter(status='new').count(),
        'total_subscribers': NewsletterSubscriber.objects.filter(is_active=True).count(),
        'total_team': TeamMember.objects.filter(is_active=True).count(),
        'total_announcements': Announcement.objects.filter(is_active=True).count(),
        'open_announcements': Announcement.objects.filter(status='open').count(),
        'total_applications': AnnouncementApplication.objects.count(),
        'total_gallery': GalleryImage.objects.filter(is_active=True).count(),
        'total_partners': Partner.objects.filter(is_active=True).count(),
        'total_testimonials': Testimonial.objects.filter(is_active=True).count(),
        'total_milestones': RoadmapMilestone.objects.filter(is_active=True).count(),
        'total_categories': ProjectCategory.objects.filter(is_active=True).count(),
        'total_gallery_cats': GalleryCategory.objects.filter(is_active=True).count(),
        'total_social_links': SocialLink.objects.filter(is_active=True).count(),
        'total_stats': CompanyStat.objects.filter(is_active=True).count(),
    }

SIDEBAR = [
    {'name':'Content', 'links':[
        ('Projects','fas fa-code','projects','total_projects'),
        ('Product Images','fas fa-images','productimages','total_product_images'),
        ('Services','fas fa-cogs','services','total_services'),
        ('Blog Posts','fas fa-newspaper','blogposts','total_blog_posts'),
        ('Testimonials','fas fa-quote-right','testimonials','total_testimonials'),
        ('Partner Logos','fas fa-handshake','partners','total_partners'),
        ('Milestones','fas fa-road','milestones','total_milestones'),
    ]},
    {'name':'Team', 'links':[
        ('Team Members','fas fa-users','teammembers','total_team'),
        ('Gallery','fas fa-images','galleryimages','total_gallery'),
        ('Gallery Categories','fas fa-tags','gallerycategories','total_gallery_cats'),
    ]},
    {'name':'Announcements', 'links':[
        ('All Announcements','fas fa-bullhorn','announcements','total_announcements'),
        ('Applications','fas fa-file-signature','applications','total_applications'),
    ]},
    {'name':'Inbox', 'links':[
        ('Contact Inquiries','fas fa-envelope','inquiries','total_inquiries'),
        ('Subscribers','fas fa-paper-plane','subscribers','total_subscribers'),
    ]},
    {'name':'Settings', 'links':[
        ('Social Links','fas fa-share-alt','sociallinks','total_social_links'),
        ('Statistics','fas fa-chart-bar','stats','total_stats'),
    ]},
]

@login_required
def portal_dashboard(request):
    s = _stats()
    context = {
        'stats': s,
        'sections': SIDEBAR,
        'recent_inquiries': ContactInquiry.objects.all().order_by('-created_at')[:5],
        'recent_applications': AnnouncementApplication.objects.all().order_by('-applied_at')[:5],
        'recent_posts': BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3],
        'open_announcements_list': Announcement.objects.filter(status='open')[:5],
        'quick_actions': [
            ('New Blog Post','fas fa-plus-circle','blogposts','create','#00f0ff'),
            ('New Project','fas fa-plus-circle','projects','create','#8b5cf6'),
            ('New Team Member','fas fa-user-plus','teammembers','create','#10b981'),
            ('New Announcement','fas fa-bullhorn','announcements','create','#ffc107'),
        ],
        'pending_count': ContactInquiry.objects.filter(status='new').count(),
    }
    return render(request, 'portal/dashboard.html', context)

# ---------------------------------------------------------------------------
#  CRUD helpers
# ---------------------------------------------------------------------------

# Model registry: what to display/list/search for each model
REGISTRY = {
    'projects': {
        'model': Project, 'icon': 'fas fa-code', 'label': 'Project',
        'list': ['name','category','status','is_featured','is_active','order'],
        'search': ['name','tagline','description'],
        'filter_map': {'category': ProjectCategory, 'status': None, 'is_active': None},
        'order': ['order'],
        'img': ['thumbnail', 'screenshot_1', 'screenshot_2', 'screenshot_3', 'banner_image'],
    },
    'productimages': {
        'model': ProductImage, 'icon': 'fas fa-images', 'label': 'Product Image',
        'list': ['project','caption','is_featured','order'],
        'search': ['caption'],
        'filter_map': {'project': Project, 'is_featured': None},
        'order': ['-is_featured','order'],
        'img': ['image'],
    },
    'categories': {
        'model': ProjectCategory, 'icon': 'fas fa-tag', 'label': 'Category',
        'list': ['name','slug','icon_class','order','is_active'],
        'search': ['name','description'],
        'order': ['order'],
    },
    'services': {
        'model': Service, 'icon': 'fas fa-cogs', 'label': 'Service',
        'list': ['name','service_type','is_featured','is_active','order'],
        'search': ['name','short_description'],
        'filter_map': {'service_type': None, 'is_active': None},
        'order': ['order'],
        'img': ['image'],
    },
    'blogposts': {
        'model': BlogPost, 'icon': 'fas fa-newspaper', 'label': 'Blog Post',
        'list': ['title','category','author','is_published','published_date'],
        'search': ['title','excerpt'],
        'filter_map': {'category': BlogCategory, 'is_published': None},
        'order': ['-published_date'],
        'img': ['featured_image'],
        'ckeditor': ['content'],
        'slug': 'title',
    },
    'blogcategories': {
        'model': BlogCategory, 'icon': 'fas fa-tags', 'label': 'Blog Category',
        'list': ['name','slug','is_active'],
        'search': ['name','description'],
        'order': ['name'],
    },
    'testimonials': {
        'model': Testimonial, 'icon': 'fas fa-quote-right', 'label': 'Testimonial',
        'list': ['client_name','client_company','rating','project','is_featured','is_active'],
        'search': ['client_name','content'],
        'order': ['-is_featured','order'],
        'img': ['client_image'],
    },
    'teammembers': {
        'model': TeamMember, 'icon': 'fas fa-users', 'label': 'Team Member',
        'list': ['name','role','order','is_active'],
        'search': ['name','role','bio'],
        'order': ['order'],
        'img': ['image'],
    },
    'announcements': {
        'model': Announcement, 'icon': 'fas fa-bullhorn', 'label': 'Announcement',
        'list': ['title','announcement_type','status','start_date','application_deadline'],
        'search': ['title','short_description'],
        'filter_map': {'announcement_type': None, 'status': None},
        'order': ['-is_featured','order','-created_at'],
        'img': ['cover_image'],
        'ckeditor': ['description'],
        'slug': 'title',
    },
    'applications': {
        'model': AnnouncementApplication, 'icon': 'fas fa-file-signature', 'label': 'Application',
        'list': ['full_name','email','announcement','status','applied_at'],
        'search': ['full_name','email','phone'],
        'filter_map': {'status': None, 'announcement': Announcement},
        'order': ['-applied_at'],
        'readonly': ['applied_at','updated_at'],
    },
    'galleryimages': {
        'model': GalleryImage, 'icon': 'fas fa-images', 'label': 'Gallery Image',
        'list': ['title','category','event_date','is_featured','is_active','order'],
        'search': ['title','description'],
        'filter_map': {'category': GalleryCategory, 'is_active': None},
        'order': ['-is_featured','order','-event_date'],
        'img': ['image'],
    },
    'gallerycategories': {
        'model': GalleryCategory, 'icon': 'fas fa-tags', 'label': 'Gallery Category',
        'list': ['name','slug','is_active','order'],
        'search': ['name','description'],
        'order': ['order'],
    },
    'partners': {
        'model': Partner, 'icon': 'fas fa-handshake', 'label': 'Partner',
        'list': ['name','website_url','is_active','order'],
        'search': ['name'],
        'order': ['order'],
        'img': ['logo'],
    },
    'milestones': {
        'model': RoadmapMilestone, 'icon': 'fas fa-road', 'label': 'Milestone',
        'list': ['year','title','is_active','order'],
        'search': ['title','description'],
        'order': ['order'],
    },
    'inquiries': {
        'model': ContactInquiry, 'icon': 'fas fa-envelope', 'label': 'Inquiry',
        'list': ['name','email','service_type','status','created_at'],
        'search': ['name','email','subject','message'],
        'filter_map': {'status': None, 'service_type': None},
        'order': ['-created_at'],
        'readonly': ['name','email','phone','service_type','subject','message','created_at','updated_at'],
    },
    'subscribers': {
        'model': NewsletterSubscriber, 'icon': 'fas fa-paper-plane', 'label': 'Subscriber',
        'list': ['email','is_active','subscribed_at'],
        'search': ['email'],
        'order': ['-subscribed_at'],
        'readonly': ['subscribed_at'],
    },
    'stats': {
        'model': CompanyStat, 'icon': 'fas fa-chart-bar', 'label': 'Statistic',
        'list': ['name','value','suffix','order','is_active'],
        'search': ['name'],
        'order': ['order'],
    },
    'sociallinks': {
        'model': SocialLink, 'icon': 'fas fa-share-alt', 'label': 'Social Link',
        'list': ['platform','icon_class','url','order','is_active'],
        'search': ['platform','url'],
        'order': ['order'],
    },
}

def _get_meta(model_name):
    return REGISTRY[model_name]

def _build_form(model, meta, data=None, files=None, instance=None):
    """Build a ModelForm for the given model/meta, handling CKEditor + images."""
    exclude = ['id']
    if 'readonly' in meta:
        exclude += meta['readonly']
    if 'slug' in meta and instance is None:
        # auto-slug on create; on edit don't exclude
        pass

    # Determine extra widgets
    widgets = {}
    if 'ckeditor' in meta:
        for fname in meta['ckeditor']:
            widgets[fname] = CKEditorUploadingWidget(config_name='blog')

    # Detect icon_class fields — use the visual icon picker
    for f in model._meta.fields:
        if f.name == 'icon_class':
            widgets[f.name] = IconPickerWidget()
            break

    FormClass = forms.modelform_factory(
        meta['model'],
        fields='__all__',
        exclude=exclude,
        widgets=widgets,
    )
    if instance:
        form = FormClass(data, files, instance=instance)
    else:
        form = FormClass(data, files)

    return form


def _get_filter_choices(meta):
    """Return list of (field_name, [(value, label), ...]) for filter dropdowns."""
    choices = []
    fm = meta.get('filter_map', {})
    for fname, fmodel in fm.items():
        if fmodel is not None:
            opts = [(str(o.pk), str(o)) for o in fmodel.objects.filter(is_active=True)] + [('','All')]
            choices.append((fname, [('','All')] + [(str(o.pk), str(o)) for o in fmodel.objects.all()]))
        else:
            # choice field on model itself
            field = meta['model']._meta.get_field(fname)
            if hasattr(field, 'choices') and field.choices:
                opts = [('','All')] + [(k,v) for k,v in field.choices]
                choices.append((fname, opts))
    return choices


def _get_display_value(obj, field_name, meta):
    """Return a display-friendly value for a field."""
    if field_name == 'category' and hasattr(obj, 'category') and obj.category:
        return str(obj.category)
    if field_name == 'project' and hasattr(obj, 'project') and obj.project:
        return str(obj.project)
    if field_name == 'announcement' and hasattr(obj, 'announcement') and obj.announcement:
        return str(obj.announcement)
    val = getattr(obj, field_name, None)
    if hasattr(obj, f'get_{field_name}_display'):
        return getattr(obj, f'get_{field_name}_display')()
    if isinstance(val, bool):
        return val
    if val is None:
        return ''
    # Truncate long text
    s = str(val)
    return s[:60] + '...' if len(s) > 60 else s


def _get_image_url(obj, meta):
    """Return first image URL found, or None."""
    for fname in meta.get('img', []):
        f = getattr(obj, fname, None)
        if f and hasattr(f, 'url'):
            return f.url
    return None


# ---------------------------------------------------------------------------
#  CRUD views
# ---------------------------------------------------------------------------

@login_required
def portal_list(request, model_name):
    meta = _get_meta(model_name)
    qs = meta['model'].objects.all()
    search_query = request.GET.get('q', '')
    if search_query:
        from django.db.models import Q
        q = Q()
        for field in meta.get('search', []):
            q |= Q(**{f'{field}__icontains': search_query})
        qs = qs.filter(q)

    # Filters
    filter_params = {}
    for fname in meta.get('filter_map', {}):
        val = request.GET.get(fname)
        if val:
            if fname in meta['filter_map'] and meta['filter_map'][fname] is not None:
                filter_params[fname] = val
            else:
                filter_params[fname] = val
    if filter_params:
        qs = qs.filter(**filter_params)

    ordering = meta.get('order', ['-id'])
    qs = qs.order_by(*ordering)

    paginator = Paginator(qs, 20)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    filter_choices = _get_filter_choices(meta)
    current_filters = {fname: request.GET.get(fname, '') for fname in meta.get('filter_map', {})}

    context = {
        'sections': SIDEBAR,
        'stats': _stats(),
        'meta': meta,
        'model_name': model_name,
        'page_obj': page_obj,
        'search_query': search_query,
        'filter_choices': filter_choices,
        'current_filters': current_filters,
        'list_fields': meta['list'],
        'total_count': qs.count(),
    }
    return render(request, 'portal/model_list.html', context)


@login_required
def portal_create(request, model_name):
    meta = _get_meta(model_name)
    if request.method == 'POST':
        form = _build_form(meta['model'], meta, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            # Auto-slug
            if 'slug' in meta and hasattr(obj, 'slug') and not obj.slug:
                from django.utils.text import slugify
                obj.slug = slugify(getattr(obj, meta['slug']))[:50]
                # ensure unique
                base = obj.slug
                n = 1
                while meta['model'].objects.filter(slug=obj.slug).exclude(pk=obj.pk).exists():
                    obj.slug = f"{base}-{n}"
                    n += 1
                obj.save(update_fields=['slug'])

            messages.success(request, f'{meta["label"]} created successfully.')
            return redirect('portal_list', model_name=model_name)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = _build_form(meta['model'], meta)

    base_ctx = {'sections': SIDEBAR, 'stats': _stats(), 'meta': meta, 'model_name': model_name}
    context = {**base_ctx,
        'form': form,
        'is_edit': False,
    }
    return render(request, 'portal/model_form.html', context)


@login_required
def portal_update(request, model_name, pk):
    meta = _get_meta(model_name)
    obj = get_object_or_404(meta['model'], pk=pk)
    if request.method == 'POST':
        form = _build_form(meta['model'], meta, data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'{meta["label"]} updated successfully.')
            return redirect('portal_list', model_name=model_name)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = _build_form(meta['model'], meta, instance=obj)

    base_ctx = {'sections': SIDEBAR, 'stats': _stats(), 'meta': meta, 'model_name': model_name}
    context = {**base_ctx,
        'form': form,
        'is_edit': True,
        'obj': obj,
    }
    return render(request, 'portal/model_form.html', context)


@login_required
def portal_delete(request, model_name, pk):
    meta = _get_meta(model_name)
    obj = get_object_or_404(meta['model'], pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f'{meta["label"]} deleted successfully.')
        return redirect('portal_list', model_name=model_name)
    base_ctx = {'sections': SIDEBAR, 'stats': _stats(), 'meta': meta, 'model_name': model_name}
    context = {**base_ctx, 'obj': obj}
    return render(request, 'portal/model_confirm_delete.html', context)


@login_required
def portal_detail(request, model_name, pk):
    """Read-only detail view (for inquiries, applications, etc.)."""
    meta = _get_meta(model_name)
    obj = get_object_or_404(meta['model'], pk=pk)
    fields = []
    readonly = meta.get('readonly', [])
    for f in meta['model']._meta.fields:
        if f.name == 'id':
            continue
        if f.name in readonly or f.name not in [x.name for x in meta['model']._meta.fields]:
            val = _get_display_value(obj, f.name, meta)
            if isinstance(val, bool):
                val = 'Yes' if val else 'No'
            if val == '' or val is None:
                val = '—'
            img_url = None
            if hasattr(obj, f.name) and hasattr(getattr(obj, f.name), 'url'):
                try:
                    img_url = getattr(obj, f.name).url
                except Exception:
                    pass
            fields.append({
                'label': f.verbose_name or f.name,
                'value': val,
                'type': type(f).__name__,
                'img_url': img_url,
            })

    # Markdown-ish value display for extra_data (JSON)
    extra = getattr(obj, 'extra_data', None)
    if extra:
        extra_items = []
        for k, v in extra.items():
            if isinstance(v, str) and v.strip():
                extra_items.append({'label': k.replace('_', ' ').title(), 'value': v})
        if extra_items:
            fields.append({'label': 'Extra Data', 'extra_items': extra_items, 'type': 'extra'})

    base_ctx = {'sections': SIDEBAR, 'stats': _stats(), 'meta': meta, 'model_name': model_name}
    context = {**base_ctx, 'obj': obj, 'fields': fields, 'readonly_fields': readonly}
    return render(request, 'portal/model_detail.html', context)
