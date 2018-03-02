from django.conf.urls import include,url
from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register(r'post', views.PostList.as_view(), base_name='post')
urlpatterns = [
    url(r'^post/$',views.PostList.as_view(),name='post-list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='post-list'),
    url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),

]