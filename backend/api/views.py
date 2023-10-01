from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

from djoser.views import UserViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    FollowValidateSerializer,
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
from recipes.constants import (
    FILE_SL,
    CONTENT,
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

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
        data = {'user': request.user.id, 'author': id}
        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowValidateSerializer(
            follow,
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        follow = Follow.objects.filter(
            user=request.user,
            author=get_object_or_404(User, id=id),
        )
        if not follow.exists():
            raise serializers.ValidationError('There is no such subscription')
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=(IsAuthenticatedOrReadOnly, ),
        serializer_class=(FollowSerializer, )
    )
    def subscriptions(self, request):
        queryset = request.user.followers.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipengredients', 'tags'
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
        slist = 'Shopping list'
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
                'errors': 'Recipe removed from favorites'
            }
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        return self.action_for_recipes(ActionsForRecipe, request.user, pk)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticatedOrReadOnly, ))
    def shopping_cart(self, request, pk=None):
        if self.request.method == 'DELETE':
            context = {
                'errors': 'Recipe removed from shopping list'
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
        response = HttpResponse(slist, content_type=CONTENT)
        response['Content-Disposition'] = f"attachment; filename='{FILE_SL}'"
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
