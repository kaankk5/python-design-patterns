from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import os
from dotenv import load_dotenv
from binance.client import Client
import time
load_dotenv()


class Publisher(ABC):

    @abstractmethod
    def attach(self, subscriber: Subscribe) -> None:
        pass

    @abstractmethod
    def detach(self, subscriber: Subscribe) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ConcretePublisher(Publisher):
    _state = None
    _subscribers: List[Subscribe] = []

    API_KEY = os.getenv('api_key')
    API_SECRET = os.getenv('api_secret')
    client = Client(API_KEY, API_SECRET)

    SYMBOL ='BTCUSDT'

    def attach(self, subscriber: Subscribe) -> None:
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def detach(self, subscriber: Subscribe) -> None:
        try:
            self._subscribers.remove(subscriber)
        except:
            ValueError()

    def notify(self) -> None:

        for subscriber in self._subscribers:
            subscriber.on_price_change(self)

    def data_stream(self):
        while True:

            ticker = self.client.get_symbol_ticker(symbol=self.SYMBOL)
            price = float(ticker['price'])
            if price != self._state:
                self._state = price
                self.notify()
            time.sleep(1)


class Subscribe(ABC):

    @abstractmethod
    def on_price_change(self,publisher:Publisher) -> None:
        pass


class ConcreteSubscriber1(Subscribe):

    def on_price_change(self,publisher:Publisher) -> None:
        print(f'Object 1:{publisher._state}')

class ConcreteSubscriber2(Subscribe):

    def on_price_change(self,publisher:Publisher) -> None:
        print(f'Object 2:{publisher._state}')


publisher = ConcretePublisher()
subs1 = ConcreteSubscriber1()
subs2 = ConcreteSubscriber2()
publisher.attach(subs1)
publisher.attach(subs2)
publisher.data_stream()

