from rest_framework import serializers

from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    ActionsForRecipe,
    RecipeIngredient,
    Ingredient,
    Follow,
    Recipe,
    User,
    Tag,
)


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
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class ActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionsForRecipe
        fields = '__all__'


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='author.id')
    email = serializers.EmailField(
        source='author.email')
    username = serializers.CharField(
        source='author.username')
    first_name = serializers.CharField(
        source='author.first_name')
    last_name = serializers.CharField(
        source='author.last_name')
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    is_subscribed = serializers.SerializerMethodField(
        read_only=True, method_name='get_is_subscribed')
    recipes_count = serializers.SerializerMethodField(
        read_only=True, method_name='get_recipes_count')

    class Meta:
        model = Follow
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'recipes',
            'recipes_count',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.all()
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


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
    image = Base64ImageField()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipengredients',
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ActionsForRecipe.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ActionsForRecipe.objects.filter(
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

    def validate_ingredient_amout(self, data):
        if not 1 <= data <= 30:
            raise serializers.ValidationError(
                'The amount of ingredient must be from 1 to 30.'
            )
        return data

    def validate_ingredient_unique(self, data):
        if not data:
            raise serializers.ValidationError(
                'Recipe must have at least 1 ingredient'
            )
        ingredients_list = []
        for ingredient in data:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    'You have already added this ingredient'
                )
            ingredients_list.append.ingredient_id
        return data

    def validate_cooking_time(self, data):
        if not 1 <= data <= 600:
            raise serializers.ValidationError(
                'The cooking time should be from 1 to 600 minutes.'
            )
        return data
