"""
URL configuration for fruitables project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from home.views import custom_404_view
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls')),
] + static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
urlpatterns+= i18n_patterns(
    path('i18n/',include('django.conf.urls.i18n')),
    path('accounts/', include('accounts.urls')),
    
    path('', include('home.urls')),
)

handler404 = custom_404_view