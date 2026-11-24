# EXAMEN 1 PARTE DIGITAL
import threading
from time import sleep
from random import randint
import queue
import math
nGallinas = 5
gallinas = []
huevos = []
sinHuevos = []
criadero = queue.Queue()
semaforoHuevo = threading.Semaphore(nGallinas)
semaforoSinHuevo = threading.Semaphore(nGallinas)
pantalla = threading.Lock()
dias = 0

def iniciar():
    global nGallinas, gallinas, huevos, sinHuevos
    for i in range(nGallinas):
        gallinas.append(threading.Thread(target=gallina,args=(f"gallina {i+1}",i,0,)))
        huevos.append(0)
        sinHuevos.append(0)
    hiloEstado = threading.Thread(target=estado)
    hiloPollitos = threading.Thread(target=pollitos)
    for x in gallinas:
        x.start()
    hiloEstado.start()
    hiloPollitos.start()
    for x in gallinas:
        x.join()
    hiloEstado.join()
    hiloPollitos.join()

def gallina(name, pos, dia):
    global nGallinas, gallinas, huevos, sinHuevos, criadero
    while dia != 365:
        posibilidadHuevo = randint(1,300)/365
        puesto = False
        if posibilidadHuevo > 0.18:
            posibilidadCriadero = randint(1,100)/100
            if posibilidadCriadero > 0.02:
                while not puesto:
                    if semaforoHuevo.acquire(timeout=2):
                        huevos[pos] += 1
                        puesto = True
                        semaforoHuevo.release()
                        if pantalla.acquire():
                            print(f"{name}, he puesto huevo")
                            pantalla.release()
            else:
                criadero.put(0)
                if pantalla.acquire():
                    print(f"{name}, mi huevo es fertil")
                    pantalla.release()
        else:
            while not puesto:
                if semaforoSinHuevo.acquire(timeout=2):
                    sinHuevos[pos] += 1
                    puesto = True
                    semaforoSinHuevo.release()
                    if pantalla.acquire():
                        print(f"{name}, no he puesto huevo")
                        pantalla.release()
        dia += 1
        sleep(randint(1,3))


def pollitos():
    global criadero, gallinas, nGallinas, huevos, sinHuevos, pantalla, semaforoHuevo, semaforoSinHuevo, dias
    while dias != 365:
        sleep(2)
        huevoCriadero = 0
        if not criadero.empty():
            size = len(list(criadero.queue))
            for x in range (size):
                huevoCriadero = criadero.get()
                if huevoCriadero != 140:
                    huevoCriadero += 1
                    criadero.put(huevoCriadero)
                else:
                    if pantalla.acquire():
                        print("Criadero detiene produccion para añadir nueva gallina")
                        pantalla.release()
                    gallinas.append(threading.Thread(target=gallina,args=(f"gallina {nGallinas+1}",nGallinas,dias,)))
                    huevos.append(0)
                    sinHuevos.append(0)
                    gallinas[nGallinas].start()
                    nGallinas += 1
        dias += 1
                    
def estado():
    global huevos, sinHuevos, criadero
    while dias != 365:
        sleep(2)
        sum = 0
        for x in huevos:
            sum += x
        porcentaje = (sum/(len(huevos)*300))*100
        porcentaje = math.ceil(porcentaje)
        if pantalla.acquire():
            print(f"Porcentaje de huevos producidos: {porcentaje}%")
            pantalla.release()

iniciar()
print("Terminado")
sum = 0
for x in huevos:
    sum += x
porcentaje = (sum/(len(huevos)*300))*100
print(f"Porcentaje de huevos producidos: {porcentaje}%, Huevos de cada gallina: {huevos}, Dias improductivos de cada gallina: {sinHuevos}, Criadero: {criadero}")