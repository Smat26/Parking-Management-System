"""panel URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='login/', permanent=False)),
    url(r'^login/$', 'staff.views.LoginUser'),
    url(r'^new/$', 'tester.views.home', name='home'),
    url(r'^main/$', 'main.views.panel'),
    url(r'^video/$', 'main.views.videofeed'),
    url(r'^logout/$', 'staff.views.LogoutUser'),
    url(r'^getRoi/$', 'main.views.getRoi'),
    url(r'^getCamera/$', 'main.views.getCamera'),
    url(r'^addroi/$', 'main.views.AddRoi'),

]
