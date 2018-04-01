"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path,include
from blog import views
from django.views.static import serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    path('login/', views.login),
    path('reg/', views.reg),
    path('get_verification_code/', views.get_verification_code),
    path('logout/', views.logout),
    path('blog/', include('blog.urls')),
    re_path('backstage/(?P<username>\w+)', views.backstage),
    re_path('add_article/', views.add_article),
    re_path('del_article/', views.del_article),
    re_path('edit_article/', views.edit_article),
    path('article_up_down/', views.article_up_down),
    path('comment/', views.comment),
    path('del_comment/', views.del_comment),
    path('comment_up/', views.comment_up),
    path('comment_up/', views.comment_up),
    path('kind/upload_img/', views.upload_img),
    path('kind/file_manager/', views.file_manager),
    # media 配置
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
