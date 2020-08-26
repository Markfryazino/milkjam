from django.shortcuts import render, redirect
from .catcher import DataCatcher
from .models import Record
import datetime
from django.utils import timezone
from .forms import TimeoutForm
from threading import Timer

start = timezone.now()
timeout = 0
catcher = None
timer = None

TIME = 12000


def zero():
    DataCatcher.active = 0


def index(request):
    global start, timeout, catcher, timer

    if request.method == "POST":
        if DataCatcher.active:
            catcher.stop()
            DataCatcher.active = 0
            timer.cancel()
        else:
            if Record.objects.all().exists():
                run_id = Record.objects.latest('time').run_id + 1
            else:
                run_id = 1

            catcher = DataCatcher(run_id, TIME)
            start, timeout = catcher.start()
            DataCatcher.active = 1
            timer = Timer(timeout, zero)
            timer.start()

        return redirect("/catcher")

    if not Record.objects.all().exists():
        return render(request, "catcher.html", {"size": Record.objects.count(),
                                                "start": start,
                                                "end": start + datetime.timedelta(seconds=timeout),
                                                "active": DataCatcher.active})
    else:
        return render(request, "catcher.html", {"size": Record.objects.count(),
                                                "latest": Record.objects.latest('time'),
                                                "last": reversed(Record.objects.order_by('-id')[:3]),
                                                "start": start,
                                                "end": start + datetime.timedelta(seconds=timeout),
                                                "active": DataCatcher.active})
