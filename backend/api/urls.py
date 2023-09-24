from django.urls import include, path
from rest_framework import routers

from api.views import (
    IngredientViewSet,
    CustomUserViewSet,
    RecipeViewSet,
    TagViewSet
)


router_v1 = routers.DefaultRouter()


router_v1.register(r'tags', TagViewSet, basename='tags'),
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients'),
router_v1.register(r'users', CustomUserViewSet, basename='users'),
router_v1.register(r'recipes', RecipeViewSet, basename='recipes'),

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
