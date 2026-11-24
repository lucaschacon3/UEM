import threading
import time
import random
import math

listaNums=[]
contante = threading.Lock()
maxVal = 100
numHilos = 3

def contar(yo):
    global maxVal
    global listaNums
    num = 0
    while num < maxVal:
        if contante.acquire(timeout=2):
            num += 1
            listaNums[yo] = num
            contante.release()
            tiempo = random.randint(2,5)/10
            time.sleep(tiempo)

def mostrar(lista):
    global maxVal
    total = 0
    while total < (maxVal*len(lista)):
        total = 0
        contante.acquire()
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
        contante.release()
        time.sleep(2)
    print("Hemos terminado de contar")


hilos = []
for i in range(0,numHilos):
    hilo = threading.Thread(target=contar,args=[i,])
    hilos.append(hilo)
    listaNums.append(0)

hilo = threading.Thread(target=mostrar,args=[listaNums,])
hilos.append(hilo)

for s in hilos:
    s.start()

for j in hilos:
    j.join()
print ("FIN")
