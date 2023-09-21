from recipes.models import (
    RecipeIngredient,
    Shopping_list,
    Ingredient,
    Favorites,
    Follow,
    Recipe,
    Tag,
    User
)
from rest_framework import serializers
from djoser.serializers import UserSerializer


REFOLLOW = 'Ты уже подписан на этого автора'
FOLLOW_YOURSELF = 'Прости, но ты не можешь подписаться на себя 💔'


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )

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
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=REFOLLOW,
            ),
        )

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                FOLLOW_YOURSELF
            )
        return data


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

# class RecipeListSerializers(serializers.ModelSerializer):
#     count = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         fields = ('count', 'name', 'measurement_unit', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipengredient',
    )
    is_favorited = serializers.SerializerMethodField()
#        method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField()
#        method_name='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Shopping_list.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()


class IngredientinRecipeCreate(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeCreateSerializers(serializers.ModelSerializer):
    ingredients = IngredientinRecipeCreate(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text', 'tags', 'ingredients')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        for ingredient_data in ingredients:
            RecipeCreateSerializers(
                recipe=instance,
                ingredient=ingredient_data('ingredient'),
                amount=ingredient_data('amount')
            )
        return super().create(validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class SlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_list
        fields = '__all__'
