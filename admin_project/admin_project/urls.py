from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-django/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
    path('', include('user_panel.urls')),
]