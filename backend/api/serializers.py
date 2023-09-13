from recipes.models import (
    Shopping_list,
    Ingredient,
    Favorites,
    Follow,
    Recipe,
    Tag,
    User
)
import webcolors
from rest_framework import serializers
from djoser.serializers import UserSerializer


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, object):
        user = self.context['request'].user
        return user.is_authenticated and Follow.objects.filter(
            following=object, user=self.context['request'].user).exists()

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
    color = Hex2NameColor()
    class Meta:
        model = Tag
        fields = '__all__'

