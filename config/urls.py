"""
URL configuration for AppointHub project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('shops/', include('apps.shops.urls')),
    path('services/', include('apps.services.urls')),
    path('staff/', include('apps.staff.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('', include(('apps.dashboard.urls', 'home'), namespace='home')),  # Root URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
