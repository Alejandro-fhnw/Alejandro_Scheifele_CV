from django.test import TestCase
from django.urls import reverse
from .models import Project

class ProjectModelTest(TestCase):
    def setUp(self):
        Project.objects.create(title="Test Project", description="Just a test")

    def test_project_creation(self):
        project = Project.objects.get(title="Test Project")
        self.assertEqual(project.description, "Just a test")

class ProjectViewTest(TestCase):
    def setUp(self):
        Project.objects.create(title="View Test Project", description="View test")

    def test_projects_page_status_code(self):
        url = reverse('projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_projects_page_contains_project(self):
        url = reverse('projects')
        response = self.client.get(url)
        self.assertContains(response, "View Test Project")