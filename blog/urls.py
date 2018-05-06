from django.conf.urls import include,url
from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, base_name='posts')
router.register(r'tags', views.TagViewSet, base_name='tags')
router.register(r'profiles', views.ProfileViewSet, base_name='profiles')
router.register(r'comments', views.CommentViewSet, base_name='comments')
# urlpatterns = [
#     url(r'^post/$',views.PostList.as_view(),name='post-list'),
#     url(r'^post/(?P<id>\d+)/$', views.PostDetail.as_view(), name='post-list'),
#     url(r'^post/(?P<slug>\w+)/$', views.PostDetail.as_view(), name='post-list'),
#     url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),
#     url(r'^comments/(?P<id>\d+)/replies/$', views.CommentListReplies.as_view(), name='comment-list-replies'),
#     url(r'^profile/$',views.ProfileList.as_view(),name='profile'),
#     url(r'^profile/(?P<handle>.+)/$',views.ProfileDetail.as_view(),name='author'),
#     url(r'^profile/(?P<name>.+)/posts$',views.PostByAuthor.as_view(),name='author-post'),
#     url(r'^profile/(?P<name>.+)/follow$',views.FollowAuthor.as_view(),name='follow-author'),
#     url(r'^tags/$',views.TagList.as_view()),
# ]

urlpatterns =router.urls