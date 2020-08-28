from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from tester.models import Run, Snapshot, run_fields


def get_name():
    if Run.objects.all().exists():
        return f"Untitled {Run.objects.all().last().id + 1}"
    else:
        return "Untitled 1"


def start_run(request):
    if request.method == 'GET':
        data = request.GET.dict()
        data = {key: val for key, val in data.items() if key in run_fields}
        if 'name' not in data:
            data['name'] = get_name()
        run = Run.objects.create(**data)
        return HttpResponse(f"Ok, run {run.name} was created")
    else:
        return HttpResponse("Invalid method")
