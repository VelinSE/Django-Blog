from io import BytesIO
from PIL import Image
from ckeditor.widgets import CKEditorWidget

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from blog.models import Post

class BlogCreationForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'}))
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'content'
        )

    def save(self, user,  commit = True):
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