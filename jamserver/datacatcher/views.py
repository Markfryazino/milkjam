from django.shortcuts import render, redirect
from .catcher import DataCatcher
from .models import Record
import datetime
from django.utils import timezone
from .forms import TimeoutForm
from threading import Timer
from plotly.offline import plot
import plotly.graph_objects as go

start = timezone.now()
timeout = 0
catcher = None
timer = None

TIME = 14400


def zero():
    DataCatcher.active = 0


def generate_plot():
    run_id = Record.objects.all().last().run_id
    data = Record.objects.all().filter(run_id=run_id)

    x = [el.timestamp for el in data]
    y = [el.price for el in data]

    trace = go.Scatter(x=x, y=y, name='price', marker_color='#995c00')
    layout = go.Layout(title="Price chart of the latest run")
    fig = go.Figure(data=[trace], layout=layout)
    plot_div = plot([trace], output_type='div', show_link=False, link_text="")
    return plot_div


def index(request):
    global start, timeout, catcher, timer

    if request.method == "POST":
        if DataCatcher.active:
            catcher.stop()
            DataCatcher.active = 0
            timer.cancel()
        else:
            if Record.objects.all().exists():
                run_id = Record.objects.all().last().run_id + 1
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
                                                "latest": Record.objects.all().last(),
                                                "last": reversed(Record.objects.order_by('-id')[:3]),
                                                "start": start,
                                                "end": start + datetime.timedelta(seconds=timeout),
                                                "active": DataCatcher.active,
                                                "plot": generate_plot()})
