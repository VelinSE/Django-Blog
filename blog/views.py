from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.forms import modelformset_factory, inlineformset_factory
from django.views import View
from django.views.generic import FormView, UpdateView

from blog.forms import BlogCreationForm, IngredientsForm, RecipeCreateForm, RecipeUpdateForm
from blog.models import Post, Ingredient

from weasyprint import HTML

class PostCreateView(FormView):
    template_name = 'CreatePost.html'
    form_class = RecipeCreateForm
    success_url = reverse_lazy('DisplayPosts')

    def form_valid(self, form):
        form = form.save(self.request.user)
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(UpdateView):
    template_name = 'UpdatePost.html'
    form_class = RecipeUpdateForm
    model = Post
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form = form.save(self.request.user)
        return super(PostUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

def display_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ingredients = get_list_or_404(Ingredient, recepie=post_id)
    return render(request, "PostDetails.html", { "post" : post, "ingredients": ingredients })

@login_required
def delete_post(request):
    post = Post.objects.get(pk=request.POST['post_id'])

    if post.user == request.user:
        post.delete()

    return redirect("/blog/posts")

def display_all_posts(request):
    posts = Post.objects.all()
    return render(request, "DisplayAllPosts.html", { "posts" : posts})

def print_post(request, post_id):
    html = HTML(request.META['HTTP_REFERER'])
    
    html.write_pdf('storage/media/test.pdf')
    

    return redirect("/blog/post/" + str(post_id))
