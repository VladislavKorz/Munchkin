from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.static import serve
from room.views import simple_chart_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/', include('room.urls')),
    path('feedback/', include('feedback.urls')),
    path('api/', include('tariff.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('test/', simple_chart_view),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
