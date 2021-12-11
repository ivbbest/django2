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
from polls.views import index, detail

from django.conf import settings
from django.conf.urls.static import static

from blogs import views
from django.urls import include, path

urlpatterns = [
    path('', index, name='index'),

    path('blog/', views.blog_handler, name='blog_handler'),
    path('page/', views.page_handler, name='page_handler'),
    path('about/', views.about_handler, name='about_handler'),
    path('index/', views.index_handler, name='index_handler'),
    path('categori/', views.categori_handler, name='categori_handler'),
    path('contact/', views.contact_handler, name='contact_handler'),
    path('latest_news/', views.latest_news, name='latest_news_handler'),
    path('robots.txt', views.robots_handler, name='robots_txt'),
    path('polls/<int:question_id>/', detail, name='detail'),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
