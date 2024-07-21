import time
import json


def measure_time(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"Время выполнения: {exec_time} сек.")

    return wrapper
