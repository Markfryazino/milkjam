from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .models import Run, Snapshot, Action


def handle_active(run, params):
    if run.duration is not None:
        params['duration'] = run.duration
        params['end_usdt'] = run.end_usdt
        params['delta_balance'] = run.end_usdt - run.start_balance
        params['active'] = 0
    else:
        last_snap = Snapshot.objects.filter(run=run).last()
        params['active'] = 1
        params['duration'] = last_snap.timestamp - run.start_time
        params['end_usdt'] = last_snap.usd_balance
        params['delta_balance'] = last_snap.usd_balance - run.start_balance


def get_action_traces(actions):
    vals = [eval(el.query)['btcusdt'] for el in actions]
    zipob = list(zip(vals, actions))
    buy_x = [el[1].snapshot.record.timestamp for el in zipob if el[0] > 0]
    sell_x = [el[1].snapshot.record.timestamp for el in zipob if el[0] < 0]
    buy_y = [el[1].snapshot.record.price for el in zipob if el[0] > 0]
    sell_y = [el[1].snapshot.record.price for el in zipob if el[0] < 0]

    buys = go.Scatter(x=buy_x, y=buy_y, marker_color='green', mode='markers', name='buys',
                      marker={'size': 10})
    sells = go.Scatter(x=sell_x, y=sell_y, marker_color='red', mode='markers', name='sells',
                       marker={'size': 10})
    return buys, sells


def usdt_plot(data):
    x = [el.timestamp for el in data]
    y = [el.usd_balance for el in data]

    fig = make_subplots()
    trace = go.Scatter(x=x, y=y, marker_color='#995c00')
    fig.add_trace(trace)
    fig.update_layout(title_text='USDT value of wallet')
    plot_div = plot(fig, output_type='div', show_link=False, link_text="")
    return plot_div


def price_plot(data, actions):
    x = [el.timestamp for el in data]
    y = [el.record.price for el in data]

    fig = make_subplots()
    trace = go.Scatter(x=x, y=y, marker_color='#995c00', name='price')
    fig.add_trace(trace)
    buys, sells = get_action_traces(actions)
    fig.add_trace(buys)
    fig.add_trace(sells)

    fig.update_layout(title_text='BTC/USDT exchange rate')
    plot_div = plot(fig, output_type='div', show_link=False, link_text="")
    return plot_div


def balances_plot(data):
    x = [el.timestamp for el in data]
    bals = [eval(el.balances) for el in data]
    y1 = [el['usdt'] for el in bals]
    y2 = [el['btc'] if 'btc' in el else 0. for el in bals]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=x, y=y1, name="USDT"), secondary_y=False)
    fig.add_trace(go.Scatter(x=x, y=y2, name="BTC"), secondary_y=True)

    fig.update_layout(title_text="USDT and BTC values")

    fig.update_xaxes(title_text="timestamp")
    fig.update_yaxes(title_text="usdt in wallet", secondary_y=False)
    fig.update_yaxes(title_text="btc in wallet", secondary_y=True)

    plot_div = plot(fig, output_type='div', show_link=False, link_text="")
    return plot_div


def index(request):
    runs = Run.objects.all()
    run = Run.objects.last()

    actions = Action.objects.filter(snapshot__run=run)
    snapshots = Snapshot.objects.filter(run=run)

    params = {'run': run, 'runs': runs, 'usdt_plot': usdt_plot(snapshots),
              'price_plot': price_plot(snapshots, actions), 'balances_plot': balances_plot(snapshots)}
    handle_active(run, params)

    params['num_actions'] = len(actions)
    params['percent_delta'] = params['delta_balance'] / run.start_balance * 100

    return render(request, 'run.html', params)
