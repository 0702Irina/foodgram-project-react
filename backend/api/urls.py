from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TagViewSet,
    RecipeViewSet,
    FollowViewSet,
    #    FavoritesViewSet,
    #   IngredientViewSet,
    # SlistViewSet
)

router = DefaultRouter()

router.register(r'^recipes', RecipeViewSet, basename='recipe')
router.register(r'^tag', TagViewSet, basename='tag')
# router.register(
#    r'^posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
# )
router.register(r'^follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]