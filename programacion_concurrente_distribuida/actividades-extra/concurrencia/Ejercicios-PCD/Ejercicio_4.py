import threading 
import time
import random


contador = 0
mutex = threading.Lock()
def contamos(nombre):
    global contador

    for i in range(1000):
        mutex.acquire()
        valor = contador
        time.sleep(random.uniform(0,.1))
        contador = valor + 1
        print(f"{contador} => contados")
        mutex.release()
    
hilos = []

for i in range(2):
    hilo = threading.Thread(target =contamos,args = ("HILO_"+str(i+1),))
    hilos.append(hilo)
    hilo.start()
for i in hilos:
    i.join()

print("CONTADOR FINALIZADO...")