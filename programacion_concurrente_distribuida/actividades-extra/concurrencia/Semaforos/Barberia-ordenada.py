import threading
import time
import random
import queue

sillas = 5
clientesEsperando = 0
listaHilos = []
listaClientes = queue.Queue()

semCliente = threading.Semaphore(5)
semPeluquero = threading.Semaphore()
sumaClientes = threading.Lock()
pantalla = threading.Lock()

def imprimir(mensaje):
    pantalla.acquire()
    print(mensaje)
    pantalla.release()

def cortarPelo():
    pantalla.acquire()
    print("\t\t",end="")
    for i in range(0,5):
        print("-",end="")
        time.sleep(1)
    print("\n",end="")
    pantalla.release()

def cliente(nombre):
    global clientesEsperando
    global sillas
    pelo = "largo"
    sumaClientes.acquire()
    if clientesEsperando <sillas:
        semCliente.acquire()
        clientesEsperando += 1
        listaClientes.put(nombre)
        sumaClientes.release()
        while pelo == "largo":
            # imprimir("El cliente "+nombre+" está esperando para cortarse el pelo")
            if semPeluquero.acquire(timeout=5):
                time.sleep(random.randint(1,3))
                pelo = "cortado"
                imprimir("El cliente "+nombre+" está listo")
            else:
                time.sleep(random.randint(1,3))
    else:
        time.sleep(random.randint(1,5))
        sumaClientes.release()
        imprimir(nombre+" NO se ha podido cortar el pelo")


def peluquero():
    global clientesEsperando
    global sillas
    while True:
        sumaClientes.acquire()
        if clientesEsperando >0:
            semCliente.release()
            cliente = listaClientes.get()
            imprimir("\t\tCortandole el pelo al cliente "+cliente)
            cortarPelo()
            clientesEsperando-=1
            
            imprimir("\t\tPelo cortado")
            imprimir(list(listaClientes.queue))
            semPeluquero.release()
            sumaClientes.release()
        else:
            sumaClientes.release()
            semPeluquero.release()
            time.sleep(random.randint(1,2))


def generarClientesNuevos():
    global listaHilos
    c=8
    while True:
        hiloCliente = threading.Thread(target=cliente,args=[str(c),])
        listaHilos.append(hiloCliente)
        listaHilos[len(listaHilos)-1].start()
        c+=1
        time.sleep(random.randint(2,7))

for c in range(1,8):
    hiloCliente = threading.Thread(target=cliente,args=[str(c),])
    listaHilos.append(hiloCliente)

hiloPeluquero = threading.Thread(target=peluquero)
listaHilos.append(hiloPeluquero)

hiloGenerador = threading.Thread(target=generarClientesNuevos)
listaHilos.append(hiloGenerador)

semPeluquero.acquire()

for s in listaHilos:
    s.start()

for s in listaHilos:
    s.join()

print("La peluquería ha cerrado")
