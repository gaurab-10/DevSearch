
from projects.models import Project, Tag
from django.db.models import Q


def searchProjects(request):
    search_query = ""
    print("search-query is:::", request.GET.get("search_query"))
    if request.GET.get('search_query') != None:
        search_query = request.GET.get("search_query")
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
         Q(title__icontains=search_query) |
         Q(owner__name__icontains=search_query) |
         Q(tags__in=tags)
        )
    return projects, search_query
