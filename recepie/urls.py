"""recepie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from recepie.views import signup, profile, protected_serve, export_excel, update_profile, change_password
from recepie.forms import LoginForm

admin.autodiscover()

urlpatterns = [
    url(r'^login$', LoginView.as_view(authentication_form=LoginForm, redirect_authenticated_user=True), name="Login"),
    url(r'^logout$', LogoutView.as_view(), name="Logout"),
    url(r'^reset-password/$', PasswordResetView.as_view(), name='reset_password'),
    url(r'^reset-password/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^signup$', signup, name="Signup"),
    url(r'^profile$', profile ,name="Profile"),
    url(r'^profile/update$', update_profile, name="ProfileUpdate"),
    url(r'^profile/update/password$', change_password, name="PasswordChange"),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="Home"),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^export_users/', export_excel, name="ExportExcel"),
    url(r'^api/', include('rest.urls'))
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
