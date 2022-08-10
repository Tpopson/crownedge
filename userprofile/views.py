from django.shortcuts import render, HttpResponse

# Create your views here.

def userprofile(request):
    return HttpResponse('Userprofile connected')