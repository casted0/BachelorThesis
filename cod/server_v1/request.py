import requests
import threading
import os

url = "curl 127.0.0.1:8080"

def curl():
    while True:
        os.system(url)

threadList = []

for i in range(5):
    t = threading.Thread(target=curl)
    t.demon = True
    threadList.append(t)

for i in range(5):
    threadList[i].start()

for i in range(5):
    threadList[i].join()