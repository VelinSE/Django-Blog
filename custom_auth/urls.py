from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import auth_login, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from custom_auth.views import register, profile, logout_user

urlpatterns = [
    url(r'^register/$', register, name="register"),
    url(r'^login/$', auth_login, { "template_name" : "login.html" } ,name='login'),
    url(r'^settings/$', profile, name = 'profile'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^reset-password/$', PasswordResetView, name='reset_password'),
    url(r'^reset-password/done/$', PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', PasswordResetCompleteView, name='password_reset_complete'),
]

