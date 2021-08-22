from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('user_profile.urls')),
    path('summernote/', include('django_summernote.urls')),

    path('', include('core.urls')),
    path('shop/', include('shop.urls')),
    path('enrolled/', include('test_manager.urls')),
    path('test/', include('test_core.urls')),
    path('blog/', include('blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

