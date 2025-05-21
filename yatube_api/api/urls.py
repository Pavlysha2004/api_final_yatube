from django.urls import path, include
from rest_framework import routers
from .views import (
    PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet
)

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post-comments'
)
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
]
