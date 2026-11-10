from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('', RedirectView.as_view(url='/news/')),
]