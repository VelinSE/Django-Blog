from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.static import serve
from django.http.response import HttpResponseForbidden
from django.http import HttpResponse
from django.core.files import File
from io import BytesIO

from blog.models import Post

from recepie.forms import SignUpForm

import xlsxwriter

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