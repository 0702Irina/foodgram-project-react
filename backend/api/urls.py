from django.urls import include, path
from rest_framework import routers

from api.views import (
    TagViewSet,
    RecipeViewSet,
    IngredientViewSet,
    SlistViewSet,
    UserViewSet
)

app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register('tags', TagViewSet, basename='tags'),
router_v1.register('slists', SlistViewSet, basename='slists'),
router_v1.register('ingredients', IngredientViewSet, basename='ingredients'),
router_v1.register('users', UserViewSet, basename='users'),
router_v1.register('recipes', RecipeViewSet, basename='recipes'),

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
]
