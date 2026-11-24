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
diasGallinas=[]
criadero=queue.Queue()
hilos=[]
gallinasInicio = 5
fracc = 10

semHuevos = threading.Semaphore()
semNoHuevos = threading.Semaphore()
semCriadero = threading.Semaphore()
semFin = threading.Semaphore()
mutexGallinas = threading.Lock()
#finAño = threading.Barrier()

def gallina(nombre,num,dias):
    global huevos
    global criadero
    global fracc
    puesto = False
    for i in range(dias):
        hayHuevo = random.randint(1,300)/365
        if hayHuevo > 0.18:
            puesto = False
            while not puesto:
                if semHuevos.acquire(timeout = 2):
                    # print(f"Gallina {num}: nuevo huevo")
                    huevos[num-1] += 1
                    diasGallinas[num-1]+=1
                    semHuevos.release()
                    
                    hayPollo = random.randint(1,300)/300
                    if hayPollo < 0.02:
                        semCriadero.acquire()
                        # print(f"Gallina {num}: nuevo pollo")
                        criadero.put(0)
                        semCriadero.release()
                    puesto = True
                else:
                    print(f"{nombre}:no ha podido guardar su huevo. Esperamos 3 seg")
                    time.sleep(3)

        else:
            puesto = False
            while not puesto:
                if semNoHuevos.acquire(timeout=2):
                    # print(f"Gallina {num}: SIN huevo")
                    sinHuevo[num-1] += 1
                    diasGallinas[num-1]+= 1
                    semNoHuevos.release()
                    puesto = True
                else:
                        print(f"{nombre}: no ha puesto huevo, pero no ha podido anotarlo. Esperamos 3 seg")
                        time.sleep(3)

        time.sleep(random.randint(1,3)/fracc)
    print(f"{nombre}: ha terminado el año.")

def pollitos():
    global criadero
    global huevos
    global sinHuevo
    global hilos
    global fracc
    i = 1
    revisado= False
    nuevaGallinaOK = False
    nuevasGallinas = 0
    nombresNuevas = ""
    while(i<=365):
        # print(f"Criadero dia {i}")
        if not criadero.empty():
            tamañoCriadero = criadero.qsize()
            nuevasGallinas = 0
            nombresNuevas= ""
            for p in range(0,tamañoCriadero):
                revisado = False
                nuevaGallinaOK = False
                while not revisado:
                    if semCriadero.acquire(timeout = 2):
                        pollo = criadero.get()
                        if pollo < 140:
                            pollo +=1
                            criadero.put(pollo)
                        else:
                            while not nuevaGallinaOK:
                                if mutexGallinas.acquire(timeout = 2):
                                    estaGallina = len(gallinas)+1
                                    dias = 365-i
                                    nombre = "Gallina " + str(estaGallina) + "(" + str(dias) + ")"
                                    gallinas.append(nombre)
                                    huevos.append(0)
                                    sinHuevo.append(0)
                                    diasGallinas.append(0)
                                    hilo = threading.Thread(target=gallina,args=["Gallina " + str(estaGallina),estaGallina,dias])
                                    hilo.start()
                                    hilos.append(hilo)
                                    mutexGallinas.release()
                                    nuevasGallinas+=1
                                    if nombresNuevas == "":
                                        nombresNuevas = nombre
                                    else:
                                        nombresNuevas = nombresNuevas + "," + nombre
                                    nuevaGallinaOK = True
                                else:
                                    print(f"CRIADERO ({i})-> " + " no hemos podido añadir la gallina " +  nombre + ". Esperamos 3 seg")
                                    time.sleep(3)
                        semCriadero.release()
                        revisado = True
                    else:
                        print(f"El dia {i} criadero no ha podido revisarse. Esperamos 3 segs.")
                        time.sleep(3)

            if nuevasGallinas > 0:
                print(f"CRIADERO ({i})-> hemos añadido {nuevasGallinas} gallinas: {nombresNuevas}")
                print(f"CRIADERO ({i})-> El gallinero queda asi: \n\tGa-{gallinas} \n\tHu-{huevos} \n\tNH-{sinHuevo}")
                print(f"CRIADERO ({i})-> El criadero  queda asi: \n \t{list(criadero.queue)}")
                # time.sleep(5)
                print("\n")
        i+=1
        time.sleep(random.randint(1,3)/fracc)
    print(f"El CRIADERO ha revisado ya los 365 días del año. No se agregan más gallinas este año.")
   

        
def mostrar():
    global huevos
    global criadero
    global finDeAñoGallinaceo
    global gallinas
    global diasGallinas
    terminar = False
    maxVal = 300
    total = 0
    mostrado = False
    criaderoMostrado = False
    semFin.acquire()
    terminar = finDeAñoGallinaceo
    semFin.release()
    while not terminar:
        total = 0
        mostrado = False
        criaderoMostrado = False
        while not mostrado:
            if semHuevos.acquire(timeout= 2):
                porcentaje = 0
                for n in huevos:
                    total += n
                porcentaje = (total*100)/(maxVal*len(huevos))
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
                print(f"GALLINAS: {gallinas}")
                print(f"    DIAS: {diasGallinas}")
                print(f"  HUEVOS: {huevos}")
                while not criaderoMostrado:
                    if semCriadero.acquire(timeout= 2):   
                        print(f"CRIADERO: {list(criadero.queue)}")
                        semCriadero.release()
                        criaderoMostrado = True
                    else:
                        print("No podemos mostrar el criadero en este momento. Esperamos 1 seg")
                        time.sleep(1)
                print("\n")
                semHuevos.release()
                time.sleep(2)
                mostrado = True
            else:
                print("No podemos mostrar el avance en este momento. Esperamos 1 seg")
                time.sleep(1)
        semFin.acquire()
        terminar = finDeAñoGallinaceo
        semFin.release()
        
            
    print("Hemos terminado de contar")


for i in range(1,gallinasInicio+1):
    nombre = "Gallina " + str(i) + "(365)"
    gallinas.append(nombre)
    huevos.append(0)
    sinHuevo.append(0)
    diasGallinas.append(0)
    hilo = threading.Thread(target=gallina,args=["Gallina " + str(i+1),i,365])
    hilos.append(hilo)

hilo = threading.Thread(target=pollitos)
hilos.append(hilo)

hiloMostrar = threading.Thread(target=mostrar)

finDeAñoGallinaceo = False

for s in hilos:
    s.start()
hiloMostrar.start()

for j in hilos:
    j.join()

finDeAñoGallinaceo = True
hiloMostrar.join()

print()
print("             Gallinas:", gallinas)
print()
print(" Dias de las gallinas:", diasGallinas)
print()
print("               Huevos:", huevos)
print()
print("            sin Huevo:", sinHuevo)
print()
print("             Criadero:", list(criadero.queue))
print()
print()
print("FIN DE AÑO")



