from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngredientViewSet,
    CustomUserViewSet,
    RecipeViewSet,
    TagViewSet
)


router = routers.DefaultRouter()


router.register(r'tags', TagViewSet, basename='tags'),
router.register(r'ingredients', IngredientViewSet, basename='ingredients'),
router.register(r'users', CustomUserViewSet, basename='users'),
router.register(r'recipes', RecipeViewSet, basename='recipes'),

urlpatterns = [
    path('/', include(router.urls)),
    path('/auth/', include('djoser.urls')),
    path('/auth/', include('djoser.urls.authtoken')),
]
