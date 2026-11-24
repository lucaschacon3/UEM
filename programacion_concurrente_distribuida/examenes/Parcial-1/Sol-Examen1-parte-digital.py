import threading
import random
import time
import queue
import math


#LAS GALLINAS PONEN 300 HUEVOS AL AÑO (365) -> 0'82%
#NUMERO ALEATORIO / 365 > 12%
gallinas=[]
huevos=[]
sinHuevo=[]
criadero=queue.Queue()
hilos=[]
gallinasInicio = 5

semHuevos = threading.Semaphore()
semNoHuevos = threading.Semaphore()
semCriadero = threading.Semaphore()
mutexGallinas = threading.Lock()
#finAño = threading.Barrier()

def gallina(num,dias):
    global huevos
    global criadero
    for i in range(dias):
        hayHuevo = random.randint(1,300)/365
        if hayHuevo > 0.18:
            semHuevos.acquire()
            # print(f"Gallina {num}: nuevo huevo")
            huevos[num-1] = huevos[num-1] +1
            semHuevos.release()
            
            hayPollo = random.randint(1,300)/300
            if hayPollo < 0.02:
                semCriadero.acquire()
                # print(f"Gallina {num}: nuevo pollo")
                criadero.put(0)
                semCriadero.release()
        else:
            semNoHuevos.acquire()
            # print(f"Gallina {num}: SIN huevo")
            sinHuevo[num-1] = sinHuevo[num-1] +1
            semNoHuevos.release()

        time.sleep(random.randint(1,3)/10)


def pollitos():
    global criadero
    global huevos
    global sinHuevo
    i = 1
    while(i<=365):
        if not criadero.empty():
            tamañoCriadero = criadero.qsize()
            for p in range(0,tamañoCriadero):
                semCriadero.acquire()
                pollo = criadero.get()
                if pollo < 140:
                    pollo +=1
                    criadero.put(pollo)
                else:
                    mutexGallinas.acquire()
                    estaGallina = len(gallinas)+1
                    dias = 365-i
                    nombre = "Gallina " + str(estaGallina) + "(" + str(dias) + ")"
                    gallinas.append(nombre)
                    huevos.append(0)
                    sinHuevo.append(0)
                    hilo = threading.Thread(target=gallina,args=[estaGallina,dias])
                    hilo.start()
                    hilos.append(hilo)
                    print("CRIADERO -> " + " metemos la gallina " +  nombre)
                    mutexGallinas.release()
                semCriadero.release()
        i+=1
        time.sleep(random.randint(1,3)/10)
   

        
def mostrar(lista):
    maxVal = 300
    total = 0
    while total < (maxVal*len(lista)):
        total = 0
        semHuevos.acquire()
        porcentaje = 0
        for n in lista:
            total += n
        porcentaje = (total*100)/(maxVal*len(lista))
        porcentaje = math.ceil(porcentaje)
        print("[",end="")
        for i in range(0,100):
            if i<= porcentaje:
                print("=",end="")
            else:
                print(" ",end="")
            i = i+10
            time.sleep(0.0005)
        print("] ",end="")
        print(str(porcentaje)+"%\n",end="")
        print(lista)
        semHuevos.release()
        time.sleep(2)
    print("Hemos terminado de contar")


for i in range(1,gallinasInicio+1):
    nombre = "Gallina " + str(i) + "(365)"
    gallinas.append(nombre)
    huevos.append(0)
    sinHuevo.append(0)
    hilo = threading.Thread(target=gallina,args=[i,365])
    hilos.append(hilo)

hilo = threading.Thread(target=pollitos)
hilos.append(hilo)

hilo = threading.Thread(target=mostrar,args=[huevos,])
hilos.append(hilo)

for s in hilos:
    s.start()

for j in hilos:
    j.join()

print()
print(" Gallinas:", gallinas)
print()
print("   Huevos:", huevos)
print()
print("sin Huevo:", sinHuevo)
print()
print(" Criadero:", list(criadero.queue))
print()
print()
print("FIN DE AÑO")



