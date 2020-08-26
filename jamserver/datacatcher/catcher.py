import multiprocessing
import threading
from binance.client import Client
from .models import Record
from binance.websockets import BinanceSocketManager
import time
from twisted.internet import reactor
from django.utils import timezone


def init_client():
    return Client('admin', 'admin')


run = 0


class DataCatcher:
    active = 0

    def callback(self, query):
        global run
        if not self.norm['norm']:
            self.finish()
            return

        price = (float(query['data']['asks'][0][0]) + float(query['data']['bids'][0][0])) / 2
        record = Record.objects.create(price=price, run_id=run)

    def __init__(self, run_id, timeout=600):
        self.manager = multiprocessing.Manager()
        self.norm = self.manager.dict()
        self.norm['norm'] = True
        self.streams = ['btcusdt@depth5']
        self.timeout = timeout
        self.manager = multiprocessing.Manager()
        self.client = init_client()

        global run
        run = run_id

        self.main_socket = BinanceSocketManager(self.client)
        self.connection_key = self.main_socket.start_multiplex_socket(self.streams, self.callback)
        self.socket_process = multiprocessing.Process(target=self.process_func)
        self.timeout_timer = None

    def finish(self):
        self.main_socket.stop_socket(self.connection_key)
        self.main_socket.close()
        reactor.stop()
        print('Datacatcher process ended')

    def stop(self):
        self.norm['norm'] = False

    def process_func(self):
        print('Datacatcher process started')
        self.timeout_timer = threading.Timer(self.timeout, self.finish)
        self.timeout_timer.start()
        self.main_socket.run()

    def start(self):
        DataCatcher.active = 1
        self.socket_process.start()
        return timezone.now(), self.timeout
