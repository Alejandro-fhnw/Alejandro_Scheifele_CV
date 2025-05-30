from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fa-code')  # z. B. 'fa-python', 'fa-html5'

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True)
    skills = models.ManyToManyField('Skill', blank=True)
    github_link = models.URLField(max_length=200, blank=True, null=True, verbose_name="GitHub Link")
    pdf_file = models.FileField(upload_to='project_pdfs/', blank=True, null=True)
    video_file = models.FileField(upload_to='project_videos/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class Experience(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} bei {self.company}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    # Neue Felder für Medien
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='blog_pdfs/', blank=True, null=True)
    video = models.FileField(upload_to='blog_videos/', blank=True, null=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class ContactInfo(models.Model):
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    social_media = models.URLField(blank=True)   # neu
    github = models.URLField(blank=True)         # neu
    transfermarkt = models.URLField(blank=True)  # neu
    # weitere Felder nach Bedarf

    def __str__(self):
        return "Contact Information"

class StaticPage(models.Model):
    name = models.CharField(max_length=100)      # z.B. "About Me"
    url_name = models.CharField(max_length=100)  # z.B. "aboutme" (wie im urls.py)
    description = models.TextField(blank=True)   # Optional: Beschreibung

    def __str__(self):
        return self.name