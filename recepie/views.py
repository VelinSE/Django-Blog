from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.static import serve
from django.http.response import HttpResponseForbidden

from blog.models import Post

from recepie.forms import SignUpForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('Profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect('Profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form' : form, "user": request.user})

@login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', { "user" : request.user})
    else:
        return redirect('Login')


def protected_serve(request, path, document_root = None, show_indexes = False):
    home_dir, filename = path.split("/")
    if home_dir == "blog_image":
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return serve(request, path, document_root, show_indexes)
                
            if request.user.has_perm('blog.view_original_img'):
                return serve(request, path, document_root, show_indexes)

            if Post.objects.filter(user=request.user).filter(image=path).count() > 0:
                return serve(request, path, document_root, show_indexes)
        return HttpResponseForbidden()

    return serve(request, path, document_root, show_indexes)