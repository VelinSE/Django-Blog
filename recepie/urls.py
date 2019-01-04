from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from recepie.views import signup, profile, protected_serve, export_excel, update_profile, change_password, HomePageView
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
    url(r'^$', HomePageView.as_view(), name="Home"),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^export_users/', export_excel, name="ExportExcel"),
    url(r'^api/', include('rest.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
