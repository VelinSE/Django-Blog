from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.static import serve
from django.core.files import File
from django.db import transaction
from django.views.generic import TemplateView

from blog.models import Post

from recepie.forms import SignUpForm, UserExtendedCreationForm, UserUpdateForm, UserExtendedUpdateForm, UserChangePasswordForm

import xlsxwriter
from io import BytesIO

def signup(request):
    if request.user.is_authenticated:
        return redirect('Profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        extended_user_form = UserExtendedCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if  extended_user_form.is_valid():
                extended_user_form.save(user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('Profile')
    else:
        form = SignUpForm()
        extended_user_form = UserExtendedCreationForm()
    return render(request, 'signup.html', {'form' : form, 'extended_user_form' : extended_user_form, "user": request.user})

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user)
    if request.user.is_authenticated:
        return render(request, 'profile.html', { "user" : request.user, "posts": posts})
    else:
        return redirect('Login')

@login_required
def change_password(request):
    if request.method == "POST":
        if request.user.has_usable_password():
            form = UserChangePasswordForm(request.user, request.POST)
        else:
            form = SetPasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('Profile')
    else: 
        if request.user.has_usable_password():
            form = UserChangePasswordForm(request.user)
        else:
            form = SetPasswordForm(request.user)
    return render(request, 'change_password.html', { 'form' : form })

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance = request.user)
        extended_user_form = UserExtendedUpdateForm(request.POST, files=request.FILES, instance=request.user.userextended)
        if user_form.is_valid() and extended_user_form.is_valid():
            user_form.save()
            extended_user_form.save()
            return redirect('Profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        extended_user_form = UserExtendedUpdateForm(instance=request.user.userextended) 
    return render(request, 'update_profile.html', {
        'user_form' : user_form,
        'extended_user_form' : extended_user_form
    })

def protected_serve(request, path, document_root = None, show_indexes = False):
    home_dir, filename = path.split("/", 1)
    if home_dir == "blog_image":
        if request.user.is_authenticated:
            if request.user.has_perm('blog.view_original_img'):
                return serve(request, path, document_root, show_indexes)

            if Post.objects.filter(user=request.user).filter(image=path).count() > 0:
                return serve(request, path, document_root, show_indexes)
        return HttpResponseForbidden()

    return serve(request, path, document_root, show_indexes)

@login_required
@permission_required('blog.run_exports')
def export_excel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True, 'default_date_format': 'dd/mm/yy'})
    worksheet = workbook.add_worksheet()
    
    users = User.objects.all()
    i = 0

    worksheet.write(i, 0, 'ID')
    worksheet.write(i, 1, 'Last Login')
    worksheet.write(i, 2, 'Superuser')
    worksheet.write(i, 3, 'Username')
    worksheet.write(i, 4, 'First Name')
    worksheet.write(i, 5, 'Last Name')

    i += 1

    for user in users:
        worksheet.write(i, 0, user.id)
        worksheet.write_datetime(i, 1, user.last_login)
        worksheet.write(i, 2, user.is_superuser)
        worksheet.write(i, 3, user.username)
        worksheet.write(i, 4, user.first_name)
        worksheet.write(i, 5, user.last_name)
        i += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=test.xlsx'
    response.write(output.read())

    return response

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        posts = Post.objects.all()
        context['posts_latest'] = posts[:6]
        context['posts_featured'] = Post.objects.filter(title__icontains='qe')[:1]
        context['posts_all'] = posts
        return context