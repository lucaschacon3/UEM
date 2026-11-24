import threading
import random
import datetime
from time import sleep
path = "file.txt"
mutex = threading.Lock()

def iniciar():
    f = open(path, 'w')
    f.write('Inicio:\n' )
    f.close()

def escribir(lineas, tiempo):
    i = 0
    while i < lineas:
        with mutex:
            x = datetime.datetime.now()
            f = open(path, "a")
            f.write("Soy " + threading.current_thread().name + " - linea " + str(i+1) + " [" + x.strftime("%H:%M:%S.%f") +"]\n")
            f.close()
        i = i+1
        sleep(random.randint(1,tiempo)/1000)
    print(threading.current_thread().name + " ha terminado")

iniciar()
hilos = []
print("Cuantos hilos quieres?")
numeroHilos = input()
print("Cuanto tiempo maximo de espera (ms) para escribir?")
tiempo = input()
print("Cuantas lineas escribe cada hilo?")
lineas = input()

for i in range (int(numeroHilos)):
    hilos.append(threading.Thread(target = escribir, args = (int(lineas), int(tiempo)),name = "hilo " + str(i+1)))

for x in hilos:
    x.start()

for x in hilos:
    x.join()