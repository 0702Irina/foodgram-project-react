# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    Shopping_list,
    Ingredient,
    Favorites,
    Follow,
    Recipe,
    Tag,
    User
)
from djoser.views import UserViewSet
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdmin
from api.serializers import (
    IngredientSerializer,
    FavoritesSerializer,
    FollowSerializer,
    RecipeSerializer,
    SlistSerializer,
    TagSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SlistViewSet(viewsets.ModelViewSet):
    queryset = Shopping_list.objects.all()
    serializer_class = SlistSerializer
