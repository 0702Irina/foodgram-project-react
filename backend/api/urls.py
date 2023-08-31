from django.urls import include, path
from rest_framework import routers

from api.views import (
    TagViewSet,
    RecipeViewSet,
    IngredientViewSet,
    SlistViewSet
)

router_v1 = routers.DefaultRouter()

router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
router_v1.register(r'tag', TagViewSet, basename='tag')
router_v1.register(r'slist', SlistViewSet, basename='slist'),
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredient'),
# router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
