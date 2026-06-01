# project_name/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.get_world_default_path if hasattr(admin, 'get_world_default_path') else admin.site.urls),
    path('api/', include('socialapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)