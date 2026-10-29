from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.http import HttpResponse

def home (request):
    return HttpResponse("Welcome to the very pretty Student Portal!")

def about(request):
    return HttpResponse("This portal manages employee routing and student services:)")

def greet(request, name):
    return HttpResponse(f"Hello, {name} Welcome to Very Pretty Portal!")
