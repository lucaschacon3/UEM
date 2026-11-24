import threading
import time 
import random
import math

lista = [0,0,0,0,0]

mutex = threading.Lock()

def contar(i,MaxValor):
    while lista[i] < MaxValor:
        mutex.acquire()
        lista[i] +=1
        mutex.release()
        print(f"Contamos => {lista}")
        tiempo = random.randint(2,5)
        time.sleep(tiempo)


def monitor(maxValor,numHilos):
    Flag = False

    while Flag == False:
        sumaTotal = sum(lista)
        porcentaje = ((sumaTotal)/(maxValor*numHilos))*100
        porcentaje = math.ceil(porcentaje)
        print(f"Monitor = {lista} => {porcentaje} %")

        if sumaTotal >= maxValor*numHilos:
            Flag = True
        else:
            time.sleep(2)


def main():

    maximoV = 5
    hilos = []
    #numeroHilos = len(lista)

    for i  in range(len(lista)):
        hilo = threading.Thread(target = contar,args=(i,maximoV))
        hilos.append(hilo)

    hilosMonitor = threading.Thread(target=monitor,args=(maximoV,len(lista)))
    hilos.append(hilosMonitor)

    for j in hilos:
        j.start()
    for j in hilos:
        j.join()

    print(f"FINAL ==> {lista}")

if __name__ == "__main__":
    main()
    