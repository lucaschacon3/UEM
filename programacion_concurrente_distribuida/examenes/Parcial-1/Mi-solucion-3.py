import threading
import time
import random
import queue


gallinas = ["G1","G2","G3","G4","G5"]
huevos = [0,0,0,0,0]
sinHuevo = [0,0,0,0,0]
criadero = queue.Queue()
diaGlobal = 0

s = threading.Semaphore(1)

def gallina(i,diaInicial = 0):

    diasAño = 365

    for a in range(diaInicial,diasAño):

        prob = random.randint(1,300)/diasAño
        s.acquire()

        if prob < 0.18:
            sinHuevo[i] +=1 
        else:
            huevos[i] += 1

            if random.random() <= 0.02:
                criadero.put(0)
        s.release()
        time.sleep(random.uniform(0.01,0.05))      


def pollitos():

    global gallinas,huevos,sinHuevo,criadero,diaGlobal

    while diaGlobal < 365:
        nuevoPollito =  queue.Queue()

        s.acquire()
        while not criadero.empty():
            edad = criadero.get()

            if edad +1 >= 140:
                indice = len(gallinas)
                gallinas.append(f"G{indice +1}")
                huevos.append(0)
                sinHuevo.append(0)
                s.release()
                gallinaNew = threading.Thread(target=gallina,args=(indice,diaGlobal))
                gallinaNew.start()
                s.acquire()
            else:
                nuevoPollito.put(edad +1)
                
        criadero = nuevoPollito
        s.release()
        diaGlobal+=1
        time.sleep(random.uniform(0.01,0.05))





hilos =[]

for i in range(len(gallinas)):

    hilo = threading.Thread(target=gallina,args=(i,))
    hilos.append(hilo)

hiloPollitos = threading.Thread(target =pollitos)
hiloPollitos.start()

for j in hilos:
    j.start()
for j in hilos:
    j.join()

hiloPollitos.join()

print("RESULTADOS")
print(f"GALLINAS => {gallinas}")
print(f"HUEVOS {huevos}")
print(f"SIN HUEVO {sinHuevo}")
print(f"CRIADERO => {criadero.qsize()} pollitos")

