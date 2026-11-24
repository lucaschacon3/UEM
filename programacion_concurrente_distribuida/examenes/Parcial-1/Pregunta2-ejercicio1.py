import threading 
import time
import random
import queue


semaforo = threading.Semaphore(1)


gallinas = ["G1","G2","G3","G4","G5"]
huevos = [0,0,0,0,0]
sinHuevo = [0,0,0,0,0]
criadero = queue.Queue()
diaGlobal = 0

def gallina(i,dia_inicio = 0):

    diasAño = 365

    for c in range(dia_inicio,diasAño):
        prob = random.randint(1,300)/diasAño
        
        semaforo.acquire()
        if prob < 0.18:
            sinHuevo[i] +=1

        else:
            huevos[i] +=1
            if random.random()<0.02:
                criadero.put(0)
        semaforo.release()

        time.sleep(random.uniform(0.01,0.05))


def pollitos():

    global gallinas,huevos,sinHuevo,diaGlobal,criadero

    while diaGlobal < 365:

        nuevosPollitos = queue.Queue()
# Zona crítica: detenemos producción para modificar listas

        semaforo.acquire()
        while not criadero.empty():
            #Sacamso el primer POLLITO
            edad = criadero.get()
            # MIENTRAS EDAD SEA >= 140 SE CONVIERTE EN GALLINA ADULTA
            if edad+1 >= 140:

                indice = len(gallinas)
                gallinas.append(f"G{indice+1}")
                #HUEVOS Y SIN HUEVO INICIALIZADOS A 0 CREAMOS NUEVAS POSICIONES
                huevos.append(0)
                sinHuevo.append(0)
                
                semaforo.release()

                hiloNuevo = threading.Thread(target=gallina,args=(indice,diaGlobal))
                hiloNuevo.start()
                semaforo.acquire()

            else:
                nuevosPollitos.put(edad+1)
        
        criadero = nuevosPollitos
        
        semaforo.release()
        diaGlobal += 1

        time.sleep(random.uniform(0.01,0.05))

def main():

    global diaGlobal

    hilos =[]

    for  i in range(len(gallinas)):
        hilo = threading.Thread(target = gallina,args=(i,))
        hilos.append(hilo)

    hilo_pollitos = threading.Thread(target=pollitos)
    hilo_pollitos.start()

    for a in hilos:
        a.start()

    for b in hilos:
        b.join()

    hilo_pollitos.join()

    print("gallinas:",gallinas)
    print("huevos por gallina:",huevos)
    print("días sin huevo:",sinHuevo)   
    print("pollitos generados (criadero):",criadero.qsize())


if __name__ == "__main__":
    main()

