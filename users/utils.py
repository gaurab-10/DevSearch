from django.db.models import Q

from users.models import Profile


def searchProfiles(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    userProfiles = Profile.objects.filter(
        # icontains == ignoreCase
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query)
    )
    return userProfiles, search_query

# def searchProjects(request):
#     search_query = ""
#     if request.GET.get('search_query'):
#         search_query = request.GET.get('search_query')
#     userProfiles = Project.objects.filter(
#         Q(name__icontains=search_query) |
#         Q(short_intro__icontains=search_query)
#     )
#     return userProfiles, search_query
