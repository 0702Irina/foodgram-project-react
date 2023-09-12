from recipes.models import (
    Shopping_list,
    Ingredient,
    Favorites,
    Follow,
    Recipe,
    Tag,
    User
)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=150
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=254
    )

    class Meta:
        fields = '__all__'
        model = User

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Recipe
        fields = '__all__'


class SlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_list
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
