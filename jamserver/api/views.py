from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from tester.models import Run, Snapshot, run_fields, Action
from datacatcher.models import Record
from django.utils import timezone
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from tester.Emulator import StupidEmulator


def get_name():
    if Run.objects.all().exists():
        return f"Untitled {Run.objects.all().last().id + 1}"
    else:
        return "Untitled 1"


def get_closest(obj, time, window=3):
    candidates = obj.objects.filter(timestamp__year=time.year,
                                    timestamp__month=time.month,
                                    timestamp__day=time.day,
                                    timestamp__hour=time.hour,
                                    timestamp__minute=time.minute,
                                    timestamp__second__gte=time.second - window,
                                    timestamp__second__lte=time.second + window)
    if not candidates.exists():
        raise ValueError("No candidates")
    else:
        print(time, timezone.make_naive(candidates[0].timestamp))

        best, val = candidates[0], abs(time - timezone.make_naive(candidates[0].timestamp))

        for cand in candidates[1:]:
            cur = abs(time - timezone.make_naive(cand.timestamp))
            if cur < val:
                best, val = cand, cur
        return best


def start_run(request):
    if request.method == 'GET':
        data = request.GET.dict()
        data = {key: val for key, val in data.items() if key in run_fields}
        if 'name' not in data:
            data['name'] = get_name()
        if 'start_balance' in data:
            data['start_balance'] = float(data['start_balance'])
        if 'start_time' not in data:
            data['start_time'] = timezone.now()
        else:
            data['start_time'] = datetime.fromisoformat(data['start_time'])
        try:
            record = get_closest(Record, data['start_time'])
        except ValueError:
            return HttpResponse("Bad times...")

        run = Run.objects.create(**data)
        last_balances = str({'usdt': run.start_balance})
        data['snapshot'] = Snapshot.objects.create(run=run, balances=last_balances,
                                                   usd_balance=run.start_balance,
                                                   timestamp=record.timestamp, record=record)
        return HttpResponse(json.dumps({'run_id': run.id}, cls=DjangoJSONEncoder))
    else:
        return HttpResponse("Invalid method")


def get_snapshot(request):
    if request.method == 'GET':
        data = request.GET.dict()
        if ('timestamp' not in data) or ('run_id' not in data):
            return HttpResponse("Required parameters missing")

        data['timestamp'] = datetime.fromisoformat(data['timestamp'])

        run = Run.objects.get(id=data['run_id'])
        if timezone.make_naive(Snapshot.objects.filter(run=run).last().timestamp) >= data['timestamp']:
            try:
                snapshot = get_closest(Snapshot, data['timestamp'])
            except ValueError:
                return HttpResponse("Bad times...")
            result = model_to_dict(snapshot)
            result['record'] = model_to_dict(snapshot.record)
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))
        else:
            last = Snapshot.objects.filter(run=run).last()

            try:
                now_record = get_closest(Record, data['timestamp'])
            except ValueError:
                return HttpResponse("Bad times...")

            for id in range(last.record.id, now_record.id + 1):
                record = Record.objects.get(id=id)
                rates = {'btcusdt': record.price}
                snapshot = Snapshot.objects.create(run=run, balances=last.balances,
                                                   usd_balance=StupidEmulator.count_usdt(eval(last.balances),
                                                                                         rates),
                                                   timestamp=record.timestamp,
                                                   record=record)
            result = model_to_dict(snapshot)
            result['record'] = model_to_dict(snapshot.record)
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))

    else:
        return HttpResponse("Invalid method")


def make_action(request):
    if request.method == 'GET':
        data = request.GET.dict()
        if ('timestamp' not in data) or ('query' not in data) or ('run_id' not in data):
            return HttpResponse("Required parameters missing")

        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        run = Run.objects.get(id=data['run_id'])
        query = eval(data['query'])

        if timezone.make_naive(Snapshot.objects.filter(run=run).last().timestamp) >= data['timestamp']:
            return HttpResponse("You are trying to change the past!")

        for key in query:
            if key not in StupidEmulator.pairs:
                return HttpResponse(f"Invalid pair {key}")

        last = Snapshot.objects.filter(run=run).last()

        try:
            now_record = get_closest(Record, data['timestamp'])
            if now_record.timestamp <= Snapshot.objects.filter(run=run).last().timestamp:
                return HttpResponse("You are trying to change the past!")
        except ValueError:
            return HttpResponse("Bad times...")

        for id in range(last.record.id, now_record.id):
            record = Record.objects.get(id=id)
            rates = {'btcusdt': record.price}
            snapshot = Snapshot.objects.create(run=run, balances=eval(last.balances),
                                               usd_balance=StupidEmulator.count_usdt(eval(last.balances),
                                                                                     rates),
                                               timestamp=record.timestamp,
                                               record=record)

        rates = {'btcusdt': now_record.price}
        delta, new_balance = StupidEmulator.make_order(eval(last.balances), query, rates)
        snapshot = Snapshot.objects.create(run=run, balances=new_balance,
                                           usd_balance=StupidEmulator.count_usdt(new_balance,
                                                                                 rates),
                                           timestamp=now_record.timestamp,
                                           record=now_record)
        action = Action.objects.create(snapshot=snapshot, query=str(query), delta=str(delta))
        result = model_to_dict(action)
        result['snapshot'] = model_to_dict(action.snapshot)
        result['snapshot']['record'] = model_to_dict(action.snapshot.record)
        return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))

    else:
        return HttpResponse('Invalid method')
