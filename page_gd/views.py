from django.shortcuts import render

# Create your views here.
def gd(request,tid):
    s=str(tid)+'.html'
    return render(request,s)