# -*- coding: utf-8 -*-
import threading
from threading import Lock
from random import randint
from time import sleep

lock = Lock()


class Bank():
    def __init__(self, balance):
        self.balance = balance

    def deposit(self):
        summ = randint(50, 500)
        self.balance += summ
        if self.balance >= 500 and lock.locked():
            lock.release()
        print(f'Пополнение: {summ}. Баланс: {self.balance}')
        sleep(0.001)

    def take(self):
        summ = randint(50, 500)
        print(f'Запрос на {summ}')
        if summ <= self.balance:
            self.balance -= summ
            print(f'Снятие: {summ}. Баланс: {self.balance}')
        else:
            print('Запрос отклонен, недостаточно средств')
            try:
                lock.acquire()
            finally:
                lock.release()
        sleep(0.001)


bk = Bank(0)


def main():
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))
    th1.start()
    th2.start()
    th1.join()
    th2.join()


for i in range(100):
    main()

print(f'Итоговый баланс: {bk.balance}')
