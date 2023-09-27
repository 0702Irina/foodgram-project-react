from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum

from djoser.views import UserViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly

from api.serializers import (
    RecipeCreateSerializers,
    RecipeShortSerializer,
    UserCreateSerializer,
    IngredientSerializer,
    FollowSerializer,
    RecipeSerializer,
    UserSerializer,
    TagSerializer,
)
from recipes.models import (
    ActionsForRecipe,
    RecipeIngredient,
    Ingredient,
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
        methods=('post',),
        permission_classes=(IsAuthenticatedOrReadOnly,)
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

    @action(
        detail=False,
        permission_classes=(IsAuthenticatedOrReadOnly, ),
        serializer_class=(FollowSerializer, )
    )
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
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipengredient', 'tags'
        ).all()
        return recipes

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializers
        return RecipeSerializer

    def action_for_recipes(self, model, user, pk):
        if self.request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            model.objects.filter(user=user, recipe__id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def create_txt_cart(self, ingredients):
        slist = 'Список покупок'
        for ingredient in ingredients:
            slist += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}"
            )
        return slist

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticatedOrReadOnly,))
    def favorite(self, request, pk=None):
        if self.request.method == 'DELETE':
            context = {
                "errors": "Рецепт удален из избранного"
            }
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        return self.action_for_recipes(ActionsForRecipe, request.user, pk)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticatedOrReadOnly, ))
    def shopping_cart(self, request, pk=None):
        if self.request.method == 'DELETE':
            context = {
                "errors": "Рецепт удален из списка покупок"
            }
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        return self.action_for_recipes(ActionsForRecipe, request.user, pk)

    @action(detail=False, methods=('GET', ))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__actions__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        slist = self.create_txt_cart(ingredients)
        file = 'slist.txt'
        response = HttpResponse(slist, content_type='text/plain')
        response['Content-Disposition'] = f"attachment; filename='{file}'"
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
