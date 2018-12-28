#!python3.6

"""IRDose URL Configuration

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
from django.urls import re_path
from django.urls import include
from django.contrib import admin
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView, LogoutView
from IRDoseApp.views import RegisterView
from django.conf import settings
from django.conf.urls.static import static

# For fileField
#from django.conf import settings
#from django.views.static import serve

#from IRDoseApp.views import (
#     IRDose_listView,
#     IRDose_createview,
#     IRDoseListView,
#     IRDoseDetailView,
#     IRDoseCreateView
#)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    re_path(r'^register/$', RegisterView.as_view(), name='register'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^IRDoseApp/', include('IRDoseApp.urls')),
    re_path(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    re_path(r'^slicer3D/$', TemplateView.as_view(template_name='slicer3D.html'), name='slicer3D'),
    re_path(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    re_path(r'^logout/$', LogoutView.as_view(template_name = 'registration/logout.html'), name='logout' ),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += [
#           url(r'^media/(?P<dcm>.*)$', serve, {
#                 'document_root': settings.MEDIA_ROOT,
#           })
#    ]
