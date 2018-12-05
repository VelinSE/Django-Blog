from blog.models import Post
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class BlogCreationForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'content'
        )

    def save(self, user,  commit = True):
        post = super(BlogCreationForm, self).save(commit=False)

        post.titile = self.cleaned_data['title']
        post.content = self.cleaned_data['content']
        post.user = user

        if commit: 
            post.save()

        return post

class PostUpdateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image'
        )

