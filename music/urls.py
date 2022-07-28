from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Sound&Soulful Admin"
admin.site.site_title = "Sound&Soulful Admin "
admin.site.index_title = "Sound&Soulful Admin"

urlpatterns = [
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),

    # API Urls
    path('v1/api/', include([
        path('', include('core.api.urls')),
        path('accounts/', include('accounts.api.urls')),
    ])),
]
