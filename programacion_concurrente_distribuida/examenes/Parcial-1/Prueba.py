import threading
import time
import random
import math

lista = [0,0,0]

mutex = threading.Lock()

def contamos(i,maxValor):

    while lista[i] < maxValor:
        mutex.acquire()
        lista[i] +=1
        mutex.release()
        tiempo = random.randint(2,5)
        time.sleep(tiempo)
        print("+++++++++++++++++++++++++++++++")
        print(f"CONTAMOS => {lista}")
        print("+++++++++++++++++++++++++++++++")


def monitor(maxValor,numeroHilos):

    flag = False

    while flag == False:
        sumaTotal = sum(lista)
        porcentaje = ((sumaTotal)/(maxValor*len(lista))*100)
        porcentaje = math.ceil(porcentaje)
        print("-----------------------------------------")
        print(f"MONITOR => {lista} PORCENTAJE => {porcentaje}%")
        print("-----------------------------")

        if sumaTotal >= maxValor*numeroHilos:
            flag = True
        else:
            time.sleep(2)

def main():
    maxValores = 10
    hilos = []
    numeroHilos = len(lista)

    for i in range(len(lista)):
        hilo = threading.Thread(target=contamos,args=(i,maxValores))
        hilos.append(hilo)

    hiloMonitor = threading.Thread(target=monitor,args=(maxValores,numeroHilos))
    hilos.append(hiloMonitor)

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    print(f"Hilo terminado => {lista}")

if __name__  == "__main__":
   main()

    