"""WebSDL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from dataloaderinterface.views import UserRegistrationView, UserUpdateView


BASE_URL = settings.SITE_URL[1:]

login_configuration = {
    'redirect_field_name': 'next'
}

logout_configuration = {
    'next_page': reverse_lazy('home')
}

password_reset_configuration = {
    'post_reset_redirect': 'password_reset_done'
}

password_done_configuration = {
    'post_reset_redirect': 'password_reset_complete'
}

urlpatterns = [
    url(r'^' + BASE_URL + 'password-reset/$', auth_views.password_reset, password_reset_configuration, name='password_reset'),
    url(r'^' + BASE_URL + 'password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^' + BASE_URL + 'password-reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, password_done_configuration, name='password_reset_confirm'),
    url(r'^' + BASE_URL + 'password-reset/completed/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^' + BASE_URL + 'admin/', admin.site.urls),
    url(r'^' + BASE_URL + 'login/$', auth_views.login, login_configuration, name='login'),
    url(r'^' + BASE_URL + 'logout/$', auth_views.logout, logout_configuration, name='logout'),
    url(r'^' + BASE_URL + 'register/$', UserRegistrationView.as_view(), name='user_registration'),
    url(r'^' + BASE_URL + 'account/$', UserUpdateView.as_view(), name='user_account'),
    url(r'^' + BASE_URL + 'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(BASE_URL, include('dataloaderinterface.urls')),
    url(BASE_URL, include('dataloaderservices.urls')),
]
