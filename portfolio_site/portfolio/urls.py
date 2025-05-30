from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('skills/', views.skills, name='skills'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),  # NEU!
    path('experience/', views.experience, name='experience'),
    path('blog/', views.blog_list, name='blog_list'),
    path('search/', views.search, name='search'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
]
