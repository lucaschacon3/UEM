import threading
from time import sleep
from random import randint

def iniciar(nClientes):
    hilos = []
    for i in range (nClientes):
        hilos.append(threading.Thread(target = taquilla, name = "cliente " + str(i+1)))
    hilos.append(threading.Thread(target = estadoTaquilla))

    for x in hilos:
        x.start()

    for x in hilos:
        x.join()

def taquilla():
    global mutex, numEntradas, entradasVendidas, fin, clientesAtendidos
    atendido = False

    print(threading.current_thread().name + " ha llegado a la taquilla del cine")

    while not atendido and not fin:

        if mutex.acquire(timeout=1):
            compra = 0
            numMax = 5

            while not atendido and not fin:

                if numMax != 1:
                    compra = randint(1,numMax)
                else:
                    compra = 1

                if compra + entradasVendidas <= numEntradas:
                    entradasVendidas += compra
                    fin = entradasVendidas == numEntradas
                    sleep(randint(1,3)/100)
                    print(threading.current_thread().name + f" ha comprado {compra} entradas")
                    atendido = True
                    clientesAtendidos += 1
                    mutex.release()
                else:
                    numMax -= 1

            if fin and not atendido:
                mutex.release()

def estadoTaquilla():
    global mutex, entradasVendidas, numEntradas, fin, clientesAtendidos, numClientes

    while numEntradas != entradasVendidas and not fin:
        anterior = entradasVendidas
        sleep(3/100)

        if mutex.acquire():
            if entradasVendidas != anterior:
                print(f"Entradas vendidas = {entradasVendidas}, Clientes Atendidos = {clientesAtendidos}")
            mutex.release()

        fin = entradasVendidas == anterior
    if entradasVendidas == numEntradas and clientesAtendidos != numClientes:
        print("Se han acabado las entradas, los clientes que no fueron antendidos se han ido")

numClientes = int(input("Introduce el numero de clientes: "))
numEntradas = int(input("Introduce la cantidad de boletos que se pueden vender: "))
mutex = threading.Lock()
entradasVendidas = 0
clientesAtendidos = 0
fin = False

iniciar(numClientes)
print("Terminamos la simulacion del cine")