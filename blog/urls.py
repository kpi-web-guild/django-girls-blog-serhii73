"""URLs for the blog app."""
from django.urls import re_path

from blog.views import PostDetail, PostEdit, PostList, PostNew

urlpatterns = [
    re_path(r'^$', PostList.as_view(), name='post_list'),
    re_path(r'^post/(?P<pk>\d+)/$', PostDetail.as_view(), name='post_detail'),
    re_path(r'^post/new/$', PostNew.as_view(), name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', PostEdit.as_view(), name='post_edit'),
]
