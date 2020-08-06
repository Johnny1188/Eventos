from django.contrib import admin
from django.urls import path, include
from . import views
from accounts import views as account_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('eventosforsd-admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('accounts/', include('accounts.urls')),
    path('rew/', include('system.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
