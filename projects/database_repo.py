
from projects.models import Project


class Repo:

    def getPosts():
        return Project.objects.all()