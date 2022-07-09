# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:47:50 2021

@author: Lenovo
"""

from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.st, name='st')
]