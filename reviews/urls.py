from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /album/
    url(r'^album$', views.album_list, name='album_list'),
    # ex: /album/5/
    url(r'^album/(?P<album_id>[0-9]+)/$', views.album_detail, name='album_detail'),
    url(r'^album/(?P<album_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
]
