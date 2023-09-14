import time
import json

def write_to_file(obj):
    with open('log.txt', 'w') as file:
        file.write(obj)


def measure_time(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        exec_time = (end_time - start_time)
        print(f'Время выполнения: {exec_time} сек.')
    return wrapper