"""
URL configuration for dury_app project.

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
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static 

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('app.urls'))
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL) 
#     # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# URL configuration for dury_app project.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('app.urls'))
    path('', include('app.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    # Removed: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Media files are now served directly from Bunny.net CDN, Django's dev server doesn't need to serve them.