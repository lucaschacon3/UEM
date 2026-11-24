import threading
from time import sleep
from random import randint
from queue import Queue

def iniciar(nProductores):
    hilos = []
    for i in range (nProductores):
        hilos.append(threading.Thread(target = depositar, name = "productor " + str(i+1)))
    for i in range(4):
        hilos.append(threading.Thread(target = recojer, args = (tiposBasura[i],), name = "consumidor " + str(i+1)))
    hilos.append(threading.Thread(target = estado))

    for x in hilos:
        x.start()

    for x in hilos:
        x.join()

def depositar():
    global cantBasura, basurero, basuraDepositada, finDepositar
    while basuraDepositada != cantBasura and not finDepositar:
        if mutex.acquire(timeout=2):
            if not finDepositar and not basurero.full():
                basurero.put(tiposBasura[randint(0,3)])
                basuraDepositada += 1
                sleep(0.5)
                print(threading.current_thread().name + ", he depositado basura")
            mutex.release()
            sleep(0.01)

    if not finDepositar:
        finDepositar = True
        bDepositar.wait()
        print("Se ha terminado de depositar basura.")
    else:
        bDepositar.wait()

def recojer(tipo):
    global cantBasura, basurero, finRecojer, tiposBasura
    print(threading.current_thread().name + f", recojo basura de tipo {tipo}")
    sleep(2)
    while not basurero.empty() or not finDepositar:
        if mutex.acquire(timeout=3):
            if not finRecojer and not basurero.empty():
                basura = basurero.get()
                if basura == tipo:
                    sleep(0.5)
                    print(threading.current_thread().name + f", he recogido basura de tipo {basura}")
                else:
                    basurero.put(basura)
                basura = ""
            mutex.release()
            sleep(0.01)

    if not finRecojer:
        finRecojer = True
        bRecoger.wait()
        print("Hemos terminado de recojer basura.")
    else:
        bRecoger.wait()

def estado():
    global basurero, finRecojer, finDepositar
    while not finDepositar or not finRecojer:
        sleep(3)
        if mutex.acquire():
            if not finDepositar or not finRecojer:
                print(f"Basura dentro: {basurero.qsize()}\nBasurero: ")
                print(basurero.queue)
            mutex.release()

nProductores = int(input("Introduce el numero de productores de basura (por defecto 4): "))
cantBasura = int(input("Introduce la cantidad de basura que quieres producir: "))
tamañoBasurero = int(input("Introduce el tamaño del basurero (por defecto 50): "))

if tamañoBasurero < 50:
    print("Cambiando al tamaño por defecto del basurero (100)")
    tamañoBasurero = 50

if nProductores < 4:
    print("Cambiando al numero por defecto de productores (4)")
    nProductores = 4

basurero = Queue(tamañoBasurero)
basuraDepositada = 0
finDepositar = False
finRecojer = False
tiposBasura = ('vidrio', 'organica', 'carton', 'plastico')
mutex = threading.Lock()
bDepositar = threading.Barrier(nProductores)
bRecoger = threading.Barrier(4)

iniciar(nProductores)
print("Terminamos la simulacion Productor - Consumidor")