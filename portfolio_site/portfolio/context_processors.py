from .models import Skill

def skills_context(request):
    skills = Skill.objects.all()
    return {'skills': skills}
