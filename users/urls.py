from django.conf.urls import url,include
from users import  views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UseViewSet, base_name='user')
urlpatterns = [
    url(r'', include(router.urls)),
]
