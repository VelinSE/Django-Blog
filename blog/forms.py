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

    def save(self, user, commit=True):
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
    metric = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'required': True}), choices={('Tbsp', 'Tbsp'), ('Tsp', 'Tsp'), ('ml', 'ml'), ('Gr', 'Gr'), ('Kg', 'Kg')}, label='Units')
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}), label='Name')

    class Meta:
        model = Ingredient
        fields = (
            'quantity',
            'metric',
            'name'
        )

    def save(self, post=None, delete=False, commit=True):
        ingredient = super(IngredientsForm, self).save(commit=False)

        if delete:
            ingredient.delete()
            return

        ingredient.recepie = post
        
        if commit:
            ingredient.save()
        
        return ingredient
    

class RecipeCreateForm(forms.Form):
    def __init__(self, instance=None, data=None, files=None, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)

        formset = modelformset_factory(Ingredient, form=IngredientsForm, min_num=1, extra=0, can_delete=True, validate_min=True)

        self.form_blog = BlogCreationForm(data=data, files=files, prefix='post', instance=instance)
        self.form_ingredient = formset(data=data, queryset=Ingredient.objects.none(), prefix='ingredient')
    
    def save(self, user, commit=True):
        post = self.form_blog.save(user)
        self.form_ingredient.save(commit=False)

        for ingredient in self.form_ingredient:
            if ingredient in self.form_ingredient.deleted_forms:
                if ingredient.instance.pk:
                    ingredient.save(delete=True)
                
            else:
                ingredient = ingredient.save(post=post)

        return post

    def is_valid(self):
        return self.form_blog.is_valid() and self.form_ingredient.is_valid()

    
class RecipeUpdateForm(RecipeCreateForm):
    def __init__(self, data=None, files=None, instance=None, *args, **kwargs):
        super(RecipeUpdateForm, self).__init__(data=data, files=files, instance=instance, *args, **kwargs)

        formset = inlineformset_factory(Post, Ingredient, min_num=1, form=IngredientsForm, extra=0, can_delete=True, validate_min=True)
        self.form_ingredient = formset(data=data, prefix='ingredient', instance=instance)
    
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
