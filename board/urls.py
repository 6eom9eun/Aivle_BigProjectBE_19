from django.urls import path, include

from . import views
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', PostViewSet) # 'posts'

app_name = 'board'
urlpatterns = [
    path('', include(router.urls)),
]

"""
    from rest_framework import routers
    router = routers.SimpleRouter()

    from .views import PostViewSet

    router.register('posts', PostViewSet)
    
"""