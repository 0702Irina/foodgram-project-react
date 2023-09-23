from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from djoser.views import UserViewSet

from rest_framework import viewsets, status
# from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from api.filters import IngredientFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    RecipeCreateSerializers,
    UserCreateSerializer,
    IngredientSerializer,
    FavoritesSerializer,
    FollowSerializer,
    RecipeSerializer,
    SlistSerializer,
    UserSerializer,
    TagSerializer,
)
from recipes.models import (
    Shopping_list,
    Ingredient,
    Favorites,
    Follow,
    Recipe,
    User,
    Tag,
)

REFOLLOW = 'Ты уже подписан на этого автора'
FOLLOW_YOURSELF = 'Очень жаль, но ты не можешь подписаться на себя 💔'


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(
        detail=True,
        methods=('post', ),
        permission_classes=(IsAuthenticated, ),
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'follow_error': FOLLOW_YOURSELF
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'follow_error': REFOLLOW
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        follow = Follow.objects.filter(
            user=request.user,
            author=get_object_or_404(User, id=id),
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            serializer_class=FollowSerializer)
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)
    # permission_classes = (IsAuthenticatedOrReadOnly,IsAuthor)

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipengredient', 'tags'
        ).all()
        return recipes

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializers
        return RecipeSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class SlistViewSet(viewsets.ModelViewSet):
    queryset = Shopping_list.objects.all()
    serializer_class = SlistSerializer
