"""URLs for the blog app."""
from django.urls import re_path

from blog.views import CreateView, EditView, ListView, TemplateView

urlpatterns = [
    re_path(r'^$', ListView.as_view(), name='post_list'),
    re_path(
        r'^post/(?P<pk>\d+)/$', TemplateView.as_view(), name='post_detail'
    ),
    re_path(r'^post/new/$', CreateView.as_view(), name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', EditView.as_view(), name='post_edit'),
]
