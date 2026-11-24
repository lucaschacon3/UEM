import time 
import random
import threading

def cualquiera():
    for i in range(100):
        time.sleep(4/100)
        print("Mas cosa")

def otra():
    for i in range(100):
        time.sleep(3/100)
        print("Mas cosa")
    

t = threading.Thread(target=cualquiera)
t2 = threading.Thread(target =cosa)
print("hola mundo")

t.start()
t2.start()
t.join()
t2.join()
