from blog.models import Post
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO

class BlogCreationForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
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
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    #   image = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image'
        )

    def Update(self):
        image = self.files['image']
        import pdb; pdb.set_trace()
        name = 'thumbnail-' + image.name
        self.instance.thumbnail = Post.ResizeImage(image, name, [500, 430])
        self.save()