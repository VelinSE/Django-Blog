from django.contrib.auth.models import User

from blog.models import Post, Ingredient
from rest_framework import serializers

class IngredientSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Ingredient
        fields = ('name', 'metric', 'quantity')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    ingredients = IngredientSerializer(many=True, allow_null=True)

    def create(self, validated_data):
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
        fields = ('id', 'title', 'content', 'cooking_time', 'servings', 'ingredients', 'user')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'posts')

