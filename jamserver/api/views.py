from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def start_run(request):
    if request.method == 'GET':
        return HttpResponse("Ok, you can start the run")
