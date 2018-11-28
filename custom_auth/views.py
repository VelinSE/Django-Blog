from django.shortcuts import render, redirect
from django.contrib.auth import logout, login

from custom_auth.models import CustomUser
from custom_auth.forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.pk is not None:
                return redirect('/accounts/profile/')
        return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'register.html', args)


def profile():
    pass

def logout_user():
    pass