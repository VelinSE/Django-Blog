from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.forms import modelformset_factory
from django.views import View

from blog.forms import BlogCreationForm, PostUpdateForm, IngredientsForm
from blog.models import Post, Ingredient

from weasyprint import HTML

# @login_required
# def create(request):
#     IngredientFormset = modelformset_factory(Ingredient, form=IngredientsForm)
#     if request.method == "POST":
#         form_blog = BlogCreationForm(request.POST, request.FILES)
#         form_ingredient = IngredientFormset(request.POST)
#         if form_blog.is_valid() and form_ingredient.is_valid():
#             user = request.user
#             post = form_blog.save(user)
#             import pdb; pdb.set_trace()
#             form_ingredient = form_ingredient.save(post)
#             return redirect("/blog/post/" + str(post.id))
#     else:
#         form_blog = BlogCreationForm()
#         form_ingredient = IngredientsForm()
#     return render(request, "CreatePost.html", { "form_blog" : form_blog, "form_ingredient" : form_ingredient })

class PostView(View):
    IngredientFormset = modelformset_factory(Ingredient, form=IngredientsForm)

    def get(self, request, *args, **kwargs):
        form_blog = BlogCreationForm()
        form_ingredient = self.IngredientFormset(queryset=Ingredient.objects.none())
        
        return render(request, "CreatePost.html", { "form_blog" : form_blog, "form_ingredient" : form_ingredient })

    def post(self, request, *args, **kwargs):
        form_blog = BlogCreationForm(self.request.POST, request.FILES)
        form_ingredient = self.IngredientFormset(self.request.POST, queryset=Ingredient.objects.none())
        
        if form_blog.is_valid() and form_ingredient.is_valid():
            user = request.user
            post = form_blog.save(user)
            
            for ingredient in form_ingredient:
                ingredient = ingredient.save(post)
                
            return HttpResponseRedirect("/blog/post/" + str(post.id))
        
        return render(request, "CreatePost.html", { "form_blog" : form_blog, "form_ingredient" : form_ingredient })
    

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

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post) 
        if form.is_valid():
            form.Update()
            return redirect("/blog/post/" + str(post.id))        
    else:
        form = PostUpdateForm(instance=post)
    return render(request, "UpdatePost.html", { "form" : form })