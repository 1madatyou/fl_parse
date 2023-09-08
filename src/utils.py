import json

def write_to_file(obj):
    with open('log.txt', 'w') as file:
        file.write(obj)