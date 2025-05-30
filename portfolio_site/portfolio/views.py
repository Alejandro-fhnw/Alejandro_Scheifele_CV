from django.shortcuts import render
from django.urls import reverse
from django.contrib.postgres.search import TrigramSimilarity
from .models import Skill, Project, Experience, BlogPost, ContactInfo, StaticPage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'portfolio/home.html')

def aboutme(request):
    return render(request, 'portfolio/aboutme.html')

def skills(request):
    all_skills = Skill.objects.all()
    return render(request, 'portfolio/skills.html', {'skills': all_skills})

def projects(request):
    all_projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': all_projects})

def experience(request):
    experiences = Experience.objects.all()
    return render(request, 'portfolio/experience.html', {'experiences': experiences})

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'portfolio/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'portfolio/blog_detail.html', {'post': post})

def contact(request):
    success = False
    contact_info = ContactInfo.objects.first()  # Erster (und einziger) Kontaktinfo-Eintrag aus Admin

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Mail an dich schicken
        send_mail(
            f'New contact from {name}',
            message + f"\n\nFrom: {name} ({email})",
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        success = True

    return render(request, 'portfolio/contact.html', {'success': success, 'contact_info': contact_info})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})

try:
    from django.contrib.postgres.search import TrigramSimilarity
    postgres_search_available = True
except ImportError:
    postgres_search_available = False

def search(request):
    query = request.GET.get('q', '').lower()
    threshold = 0.2

    if postgres_search_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        results_projects = Project.objects.annotate(
            similarity_title=TrigramSimilarity('title', query),
            similarity_description=TrigramSimilarity('description', query),
        ).filter(
            Q(similarity_title__gt=threshold) | Q(similarity_description__gt=threshold)
        ).order_by('-similarity_title', '-similarity_description')

        results_experience = Experience.objects.annotate(
            similarity_job=TrigramSimilarity('job_title', query),
            similarity_company=TrigramSimilarity('company', query),
            similarity_description=TrigramSimilarity('description', query),
        ).filter(
            Q(similarity_job__gt=threshold) | Q(similarity_company__gt=threshold) | Q(similarity_description__gt=threshold)
        ).order_by('-similarity_job', '-similarity_company', '-similarity_description')

        results_skills = Skill.objects.annotate(
            similarity_name=TrigramSimilarity('name', query),
            similarity_description=TrigramSimilarity('description', query),
            similarity_category=TrigramSimilarity('category', query),
        ).filter(
            Q(similarity_name__gt=threshold) | Q(similarity_description__gt=threshold) | Q(similarity_category__gt=threshold)
        ).order_by('-similarity_name', '-similarity_description', '-similarity_category')

        results_blogposts = BlogPost.objects.annotate(
            similarity_title=TrigramSimilarity('title', query),
            similarity_content=TrigramSimilarity('content', query),
        ).filter(
            Q(similarity_title__gt=threshold) | Q(similarity_content__gt=threshold)
        ).order_by('-similarity_title', '-similarity_content')
    else:
        # Fallback auf SQLite - einfache icontains Suche ohne similarity
        results_projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        results_experience = Experience.objects.filter(
            Q(job_title__icontains=query) | Q(company__icontains=query) | Q(description__icontains=query)
        )

        results_skills = Skill.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )

        results_blogposts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Statische Seiten aus der DB holen, gefiltert nach Suchbegriff
    static_pages = StaticPage.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'results_projects': results_projects,
        'results_experience': results_experience,
        'results_skills': results_skills,
        'results_blogposts': results_blogposts,
        'static_pages': static_pages,
    }

    return render(request, 'portfolio/search_results.html', context)