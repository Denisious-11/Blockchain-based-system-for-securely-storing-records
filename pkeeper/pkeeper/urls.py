"""pkeeper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from pkeeper_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$',display_login),
    url(r'^display_login', display_login, name="display_login"),
    url(r'^logout', logout, name="logout"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^show_home_admin', show_home_admin, name="show_home_admin"),
    url(r'^register', register, name="register"),
    url(r'^view_requests', view_requests, name="view_requests"),
    url(r'^display_users', display_users, name="display_users"),
    url(r'^approve1', approve1, name="approve1"),
    url(r'^reject1', reject1, name="reject1"),
    url(r'^show_home_user', show_home_user, name="show_home_user"),
    url(r'^display_upload_data', display_upload_data, name="display_upload_data"),
    url(r'^upload_file', upload_file, name="upload_file"),
    url(r'^view_records', view_records, name="view_records"),
    url(r'^collect', collect, name="collect"),
    url(r'^temp_del',temp_del,name="temp_del"),
]
