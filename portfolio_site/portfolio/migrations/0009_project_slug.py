# Generated by Django 5.2.1 on 2025-05-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0008_contactinfo_github_contactinfo_social_media_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
