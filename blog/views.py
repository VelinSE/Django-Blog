from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect
from django.forms import modelformset_factory, inlineformset_factory
from django.views import View
from django.views.generic.edit import FormView, UpdateView

from blog.forms import BlogCreationForm, PostUpdateForm, IngredientsForm, RecipeCreateForm, RecipeUpdateForm
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

    # class PostCreateView(View):
    #     # IngredientFormset = modelformset_factory(Ingredient, form=IngredientsForm, min_num=1, extra=0, can_delete=True, validate_min=True)

    #     def get(self, request, *args, **kwargs):
    #         # form_blog = BlogCreationForm()
    #         # form_ingredient = self.IngredientFormset(queryset=Ingredient.objects.none(), prefix='ingredient')
    #         recipe_form = RecipeCreateForm()

    #         return render(request, "CreatePost.html", { "recipe_form" : recipe_form })

    #     def post(self, request, *args, **kwargs):
    #         # form_blog = BlogCreationForm(self.request.POST, request.FILES)
    #         # form_ingredient = self.IngredientFormset(self.request.POST, queryset=Ingredient.objects.none(), prefix='ingredient')
    #         recipe_form = RecipeCreateForm(self.request.POST, self.request.FILES)
    #         #import pdb; pdb.set_trace()
    #         if recipe_form.is_valid():
    #             #import pdb; pdb.set_trace()
    #             post = recipe_form.save(request.user)
                    
    #             return HttpResponseRedirect("/blog/post/" + str(post.id))
            
    #         return render(request, "CreatePost.html", { "recipe_form": recipe_form })

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

@login_required
def update_post(request, post_id):
    IngredientFormset = inlineformset_factory(Post, Ingredient, form=IngredientsForm, min_num=1, extra=0, can_delete=True, validate_min=True)
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post) 
        if form.is_valid():
            form.Update()
            return redirect("/blog/post/" + str(post.id))        
    else:
        form_blog = BlogCreationForm(instance=post)
        form_ingredient = IngredientFormset(queryset=Ingredient.objects.filter(recepie=post_id), prefix='ingredient')
    return render(request, "UpdatePost.html", { "form_blog" : form_blog, "form_ingredient" : form_ingredient })