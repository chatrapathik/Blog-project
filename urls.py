from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^upload', views.upload, name="upload blog"),
    url(r'^view', views.view, name="blog viewed"),
    url(r'^like', views.like, name="blog liked"),
    url(r'^unlike', views.unlike, name="blog unliked"),
    url(r'^comment', views.comment, name="commented on blog"),
    url(r'^list_blogs', views.list_blogs, name="List all the blogs"),
    url(r'blog_info', views.blog_info, name="get blog info")
]
