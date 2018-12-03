from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blog.forms import BlogCreationForm
from blog.models import Post
# Create your views here.

@login_required
def create(request):
    if request.method == "POST":
        form = BlogCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            post = form.save(user)
            return redirect("/blog/post/" + str(post.id))
    else:
        form = BlogCreationForm()
    return render(request, "CreatePost.html", { "form" : form })
    

def display_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, "PostDetails.html", { "post" : post })

@login_required
def delete_post(request):
    post = Post.objects.get(pk=request.POST['post_id'])

    import pdb; pdb.set_trace()
    if post.user == request.user:
        post.delete()

    return redirect("/blog/posts")

def display_all_posts(request):
    posts = Post.objects.all()
    return render(request, "DisplayAllPosts.html", { "posts" : posts})
