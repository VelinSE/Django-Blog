from io import BytesIO
from PIL import Image
from ckeditor.widgets import CKEditorWidget

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from blog.models import Post, Ingredient

class BlogCreationForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    cooking_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    servings = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'content',
            'cooking_time',
            'servings',
        )

    def save(self, user, commit = True):
        post = super(BlogCreationForm, self).save(commit=False)

        name = 'thumbnail-' + post.image.name
        resized_image = Post.ResizeImage(post.image, name, [500, 430])  

        post.user = user  
        post.thumbnail.save(name, resized_image)
        
        if commit: 
            post.save()

        return post

class IngredientsForm(ModelForm):
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}), label='Quantity')
    metric = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'required': True}), choices={('Tbsp', 'Tbsp'), ('Tsp', 'Tsp'), ('ml', 'ml')}, label='Units')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}), label='Name')

    class Meta:
        model = Ingredient
        fields = (
            'quantity',
            'metric',
            'name'
        )

    def save(self, post, commit=True):
        ingredient = super(IngredientsForm, self).save(commit=False)
        ingredient.recepie = post

        if commit:
            ingredient.save()
        
        return ingredient

class PostUpdateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'}))
    #image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    cooking_time = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    servings = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'cooking_time',
            'servings',
            'content',
            'image',
        )

    def Update(self):
        if bool(self.files):
            image = self.files['image']
            name = 'thumbnail-' + image.name
            self.instance.thumbnail = Post.ResizeImage(image, name, [500, 430])
            
        self.save()