from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Dream Homes"
admin.site.site_title = "Dream Homes:Property Management System"
admin.site.index_title = "Welcome to Dream Homes Portal"

handler404 = 'pms.views.error_404_view'
