from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest

from blog.forms import BlogCreationForm, PostUpdateForm
from blog.models import Post

from weasyprint import HTML

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
    post = get_object_or_404(Post, id=post_id)
    return render(request, "PostDetails.html", { "post" : post })

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