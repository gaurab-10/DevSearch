
from django.urls import path
from . import views
urlpatterns = [
    path('', views.showProjects, name="projects"),
    path('project/<str:pk>/', views.loadProject, name="project"),
    path('createProject/', views.createProject, name="create-project"),
    path('updateProject/<str:pk>/', views.updateProject, name="update-project"),
    path('deleteProject/<str:pk>/', views.deleteProject, name="delete-project"),
]
