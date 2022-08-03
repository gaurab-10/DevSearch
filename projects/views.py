from importlib.metadata import PackageNotFoundError
from django.http import HttpResponse
from django.shortcuts import redirect, redirect, render
from django.contrib.auth.decorators import login_required
from projects.database_repo import Repo
from projects.models import Project
from projects.utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProjectForm

# Create your views here.

# Type of request is WSGIRequest


def showProjects(request):
    # return HttpResponse("Here are our products")
    projects, search_query = searchProjects(request)
    page = request.GET.get("page")
    items = 3
    # i want 3 results per page.
    paginator = Paginator(projects, items)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    return render(request, 'projects/projects.html', {"projects": projects, 
                                                    "search_query": search_query, 
                                                    "paginator": paginator
    })


def loadProject(request, pk):
    # return HttpResponse("Single projects  "+str(pk))
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    return render(request, 'projects/single-project.html', {"project": projectObj, "tags": tags})


# If user tries to excess this view python will check first whether the user is
# logged in or not. If not then it will redirect the user to the login page.
@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
      #  print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            # Getting the currently logged in user.
            project.owner = request.user.profile
            project.save()
            # name of the url
            return redirect('projects')
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):

    project = Project.objects.get(id=pk)
    # we need to pass the instance here to show it's details in the form
    form = ProjectForm(instance=project)
    if request.method == "POST":
       # print(request.POST)
       # we need to pass the instance here otherwise it will create the new project
       # with reference to the project we passed in the form inputs.
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
