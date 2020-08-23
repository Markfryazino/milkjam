from django.shortcuts import render
from .catcher import DataCatcher
from .models import Record


def index(request):
    if request.method == "POST":
        Record.objects.all().delete()
        catcher = DataCatcher(10)
        catcher.start()

    return render(request, "catcher.html", {"records": Record.objects.all()})
