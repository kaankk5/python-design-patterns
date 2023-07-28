from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Publisher(ABC):
    @abstractmethod
    def attach(self, subscriber: Subscriber) -> None:
        pass

    @abstractmethod
    def detach(self, subscriber: Subscriber) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ConcretePublisher(Publisher):
    _state = None
    _subscribers: List[Subscriber] = []

    def attach(self, subscriber: Subscriber) -> None:
        self._subscribers.append(subscriber)

    def detach(self, subscriber: Subscriber) -> None:
        self._subscribers.remove(subscriber)

    def notify(self) -> None:

        for subscriber in self._subscribers:
            subscriber.update(self)

    def business_logic(self):
        count = 0
        while True:
            random_number = randrange(0, 10)
            self._state = random_number
            if self._state > 5:
                self.notify()
                count +=1


class Subscriber(ABC):
    @abstractmethod
    def update(self, publisher: Publisher):
        pass


class ConcereteSubscriber1(Subscriber):

    def update(self, publisher: Publisher):
        print(f'Object1 : {publisher._state}')


class ConcereteSubscriber2(Subscriber):

    def update(self, publisher: Publisher):
        print(f'Object2 : {publisher._state}')



concere_sub1 = ConcereteSubscriber1()
concere_sub2 = ConcereteSubscriber2()

concerete_publisher = ConcretePublisher()

concerete_publisher.attach(concere_sub1)
concerete_publisher.business_logic()





