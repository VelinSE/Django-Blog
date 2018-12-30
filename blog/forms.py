from io import BytesIO
from PIL import Image
from ckeditor.widgets import CKEditorWidget

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from blog.models import Post, Ingredient

class BlogCreationForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'content'
        )

    def save(self, user, commit=True):
        post = super(BlogCreationForm, self).save(commit=False)

        name = 'thumbnail-' + post.image.name
        resized_image = Post.ResizeImage(post.image, name, [500, 430])  

        post.user = user  
        post.thumbnail.save(name, resized_image)
        
        if commit: 
            post.save()

        return post

class PostUpdateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'}))
    #image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image'
        )

    def Update(self):
        image = self.files['image']
        name = 'thumbnail-' + image.name
        self.instance.thumbnail = Post.ResizeImage(image, name, [500, 430])
        self.save()

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

class RecipeCreateForm(forms.Form):
    IngredientFormset = modelformset_factory(Ingredient, form=IngredientsForm, min_num=1, extra=0, can_delete=True, validate_min=True)

    def __init__(self, data=None, files=None, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)

        self.form_blog = BlogCreationForm(data=data, files=files, prefix="post")
        self.form_ingredient = self.IngredientFormset(data=data, queryset=Ingredient.objects.none(), prefix='ingredient')
    
    def save(self, user, commit=False):
        post = self.form_blog.save(user)
        for ingredient in self.form_ingredient:
                #import pdb; pdb.set_trace()
                ingredient = ingredient.save(post)

        return post

    def is_valid(self):
        return self.form_blog.is_valid() and self.form_ingredient.is_valid()
#class IngredientsUpdateForm(ModelForm, IngredientsForm):
    