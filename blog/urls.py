from django.conf.urls import include,url
from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register(r'post', views.PostList.as_view(), base_name='post')
urlpatterns = [
    url(r'^post/$',views.PostList.as_view(),name='post-list'),
    url(r'^post/(?P<slug>.+)/$', views.PostDetail.as_view(), name='post-list'),
    url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^profile/$',views.ProfileDetail.as_view(),name='profile'),
    url(r'^profile/(?P<handle>.+)$',views.ProfileDetail.as_view(),name='author-post'),
    url(r'^author/(?P<name>.+)/posts',views.PostByAuthor.as_view(),name='author-post')

]