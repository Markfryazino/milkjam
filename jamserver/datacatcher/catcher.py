import multiprocessing
import threading
from binance.client import Client
from .models import Record
from binance.websockets import BinanceSocketManager
import time
from twisted.internet import reactor


def init_client():
    return Client('admin', 'admin')


def callback(query):
    price = (float(query['data']['asks'][0][0]) + float(query['data']['bids'][0][0])) / 2
    record = Record.objects.create(price=price)


class DataCatcher:
    def __init__(self, timeout=600):
        self.streams = ['btcusdt@depth5']
        self.timeout = timeout
        self.manager = multiprocessing.Manager()
        self.client = init_client()

        self.main_socket = BinanceSocketManager(self.client)
        self.connection_key = self.main_socket.start_multiplex_socket(self.streams, callback)
        self.socket_process = multiprocessing.Process(target=self.process_func)

    def finish(self):
        self.main_socket.stop_socket(self.connection_key)
        self.main_socket.close()
        reactor.stop()
        print('Datacatcher process ended')

    def process_func(self):
        print('Datacatcher process started')
        timeout_timer = threading.Timer(self.timeout, self.finish)
        timeout_timer.start()
        self.main_socket.run()

    def start(self):
        self.socket_process.start()
