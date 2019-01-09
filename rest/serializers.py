from django.contrib.auth.models import User

from blog.models import Post, Ingredient
from recepie.models import UserExtended
from rest_framework import serializers

class UserExtendedSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExtended
        fields = ['profile_image']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'metric', 'quantity')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    ingredients = IngredientSerializer(many=True, allow_null=True, required=False)

    def create(self, validated_data):
        ingredients_validated = []
        if 'ingredients' in validated_data.keys():
            ingredients_validated = validated_data.pop('ingredients')
        
        post = Post.objects.create(**validated_data)
        
        for ingredient_data in ingredients_validated:
            Ingredient.objects.create(recepie=post, **ingredient_data)
        
        return post

    def update(self, instance, validated_data):
        ingredients_validated = validated_data.pop('ingredients')
        ingredients_new = list()

        for ingredient_data in ingredients_validated:
            ingredients_new.append(Ingredient.objects.create(recepie=instance, **ingredient_data))

        for ingredient in instance.ingredients.get_queryset():
            if ingredients_new:
                if ingredient not in ingredients_new:
                    ingredient.delete()

        
        instance.ingredients.set(ingredients_new)
        
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.cooking_time = validated_data['cooking_time']
        instance.servings = validated_data['servings']

        return instance

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'cooking_time', 'servings', 'ingredients', 'image', 'user')
        extra_kwargs = {'image': {'required': False}}

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)
    userextended = UserExtendedSerializer(many=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.context['view'].action == 'update':
            self.fields['username'].read_only = True
            self.fields['password'].read_only = True

    def create(self, validated_data):
        userextended_validated = validated_data.pop('userextended')
        
        user = User.objects.create(**validated_data)
        
        user.userextended.profile_image = userextended_validated['profile_image']
        user.save()

        return user

    def update(self, instance, validated_data):
        userextended_validated = validated_data.pop('userextended')
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.userextended.profile_image = userextended_validated['profile_image']

        instance.save()

        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'posts', 'userextended',)

