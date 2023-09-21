# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from recipes.models import (
    Shopping_list,
    Ingredient,
    Favorites,
    Recipe,
    Tag,
    User
)
from djoser.views import UserViewSet
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
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
    TagSerializer,
    UserSerializer
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


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

    # def list(self, request):

    #     return super().list(request)


class FollowViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter
    )
    search_fields = ('user__username', 'following__username')
    filterset_fields = ('user', 'following')

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
