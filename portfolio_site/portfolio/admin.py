from django.contrib import admin
from .models import Person, Skill, Project, Experience, BlogPost, ContactInfo, StaticPage

admin.site.register(Person)
admin.site.register(Experience)
admin.site.register(StaticPage)
#admin.site.register(ContactInfo)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)
    list_display = ('title', 'github_link',)
    fields = ('title', 'description', 'skills', 'image', 'pdf_file', 'video_file', 'github_link')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email', 'linkedin', 'twitter', 'social_media', 'github', 'transfermarkt')