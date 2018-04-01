from django.urls import path, re_path
from . import views
urlpatterns = [
    path('<str:user_site>/', views.home_site),
    path('<str:user_site>/article/<int:article_id>', views.article_detail),
    re_path('(?P<user_site>\w+)/(?P<condition>homecategory|tag|date)/(?P<para>(\w|-|%|:| )+)', views.home_site),
]