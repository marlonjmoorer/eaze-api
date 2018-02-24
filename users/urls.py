from django.conf.urls import url,include
from users import  views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UseViewSet, base_name='user')
urlpatterns = [
   ## url(r'^users/$', views.UseViewSet),
    # url(r'^posts/$', views.PostList.as_view()),

    ##url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'', include(router.urls)),
]
