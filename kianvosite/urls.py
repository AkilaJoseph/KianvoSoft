from django.urls import path, re_path
from . import views
from . import portal_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.project_detail, name='project_detail'),
    path('products/', views.products, name='products'),
    path('gallery/', views.gallery, name='gallery'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/<slug:slug>/', views.announcement_detail, name='announcement_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('team/', views.team, name='team'),
    path('partners/', views.partners, name='partners'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # Portal
    path('portal/login/', portal_views.portal_login, name='portal_login'),
    path('portal/logout/', portal_views.portal_logout, name='portal_logout'),
    path('portal/dashboard/', portal_views.portal_dashboard, name='portal_dashboard'),
    path('portal/', portal_views.portal_login),

    # Portal CRUD
    path('portal/<slug:model_name>/', portal_views.portal_list, name='portal_list'),
    path('portal/<slug:model_name>/create/', portal_views.portal_create, name='portal_create'),
    path('portal/<slug:model_name>/<int:pk>/', portal_views.portal_detail, name='portal_detail'),
    path('portal/<slug:model_name>/<int:pk>/edit/', portal_views.portal_update, name='portal_update'),
    path('portal/<slug:model_name>/<int:pk>/delete/', portal_views.portal_delete, name='portal_delete'),
]
