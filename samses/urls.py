
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('account/', include('users.urls', namespace='users')),
    path('schools/', include('schools.urls', namespace='schools')),
    # path('students/', include('students.urls', namespace='students')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    # path('accounts/', include('django.contrib.auth.urls')),

] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)