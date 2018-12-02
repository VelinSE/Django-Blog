from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from recepie.forms import SignUpForm

def signup(request):
    if request.user.is_auhenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form' : form})

@login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', { "user" : request.user})
    else:
        return redirect('login')