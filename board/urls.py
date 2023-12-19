from django.urls import path
from rest_framework import routers
router = routers.SimpleRouter()

from .views import PostViewSet

router.register('posts', PostViewSet)

urlpatterns = router.urls