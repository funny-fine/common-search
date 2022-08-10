# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 14:33:56 2021

@author: Lenovo
"""

from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.page0, name='page0')
]