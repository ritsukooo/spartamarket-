
from django.contrib import admin
from django.urls import path
from products import views
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index, name='index'),
    
    
    path("products/", include("products.urls")),
    path("accounts/", include("accounts.urls")),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)