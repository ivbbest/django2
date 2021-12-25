"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import debug_toolbar
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blogs import views
from django.urls import include, path


urlpatterns = [
    path('', views.index_handler, name='homepage'),
    path('blog/', views.blog_handler, name='blog'),
    path('<slug>', views.category_handler, name='category'),
    path('post/<slug>', views.page_handler, name='article'),
    path('about/', views.about_handler, name='about'),
    path('category/', views.category_handler, name='category_old'),
    path('contact/', views.contact_handler, name='contact'),
    path('latest_news/', views.latest_news, name='latest_news'),
    path('robots.txt', views.robots_handler, name='robots_txt'),

    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
