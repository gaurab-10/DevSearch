
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Go the folder projects and include all the urls from the urls.py inside projects foldres.
    path('projects/', include('projects.urls')),
    path('', include('users.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)