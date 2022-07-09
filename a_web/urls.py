"""a_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include,path
from wpage0 import views as vw
from page_st import views as vp
from avdance import views as va
from page_gd import views as vp_gd

urlpatterns = [
    #path('wpage0/', include('wpage0.urls')),
    path('page_st/', vp.st, name='st'),
    path('avdance/',va.st1, name='st1'),
    path('wpage0/', vw.page0, name='page0'),
    path('page_gd/gd/<tid>', vp_gd.gd, name='gd'),
    path('admin/', admin.site.urls),
]
