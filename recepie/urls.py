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
from django.contrib.auth.views import LoginView, LogoutView 
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from recepie.views import signup, profile

urlpatterns = [
    url(r'^login$', LoginView.as_view(), name="Login"),
    url(r'^logout$', LogoutView.as_view(), name="Logout"),
    url(r'^signup$', signup, name="Signup"),
    url(r'^profile$', profile,name="Profile"),
    url(r'^home$', TemplateView.as_view(template_name="home.html"), name="Home"),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
