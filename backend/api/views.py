# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    Shopping_list,
    Ingredient,
    Favorites,
    Follow,
    Recipe,
    Tag
)
from rest_framework import viewsets
# from rest_framework.filters import SearchFilter
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import IsAuthenticated

# from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    FavoritesSerializer,
    FollowSerializer,
    RecipeSerializer,
    SlistSerializer,
    TagSerializer
)


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
