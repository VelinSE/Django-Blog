from blog.models import Post
from django.contrib.auth.models import User
from django.forms import ModelForm

class BlogCreationForm(ModelForm):

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

