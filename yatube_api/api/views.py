from django.shortcuts import get_object_or_404
from .permissions import AuthorOrReadOnly, ReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer,
    FollowSerializer)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('user__username', 'following__username')
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        following = serializer.validated_data['following']
        if user == following:
            raise ValidationError("Нельзя подписаться на самого себя.")
        serializer.save(user=user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.order_by('-created')

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
