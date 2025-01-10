
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from backend.samses_views import home_view, dashboard

urlpatterns = [
    
    path('admin/', admin.site.urls),
    # path('account/', include('backend.users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),

    path('schools/', include('backend.schools.urls', namespace='schools')),
    path('student/', include('backend.student.urls', namespace='student')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', home_view),
    path('/dashboard', dashboard, name="dashboard"),
    # path('accounts/', include('django.contrib.auth.urls')),

] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)