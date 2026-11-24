import time
import random
import threading

sumaTotal = 0
cuantos = 100 
cuantosHilos = 10
resultadoHilos = []
mutex = threading.Lock()
def suma(nombre, cuantos,operador):
    global sumaTotal
    global resultadoTotal
    tiempoHilo0 =  time.time()
    tiempoSuma0 = 0
    tiempoSuma1 = 0
    tiempoSuma2 = 0
    for i in range(cuantos):
        sumaPre = sumaTotal
        tiempoSuma0 =  time.time()
        if operador == "sumado":
            if mutex.acquire():
                sumaTotal += 1
                mutex.release()
        elif operador == "restado":
            sumaTotal -= 1
            mutex.release()
        else:
            print("Mal llamado sin 'suma' ni 'resta'")
        #sumaTotal += 1
        tiempoSuma1 = time.time()
        tiempoEspera = random.randint(1,3)/10
        tiempoSuma2 = time.time()
        time.sleep(tiempoEspera)
        print(f"{nombre}: ha sumado 1 {sumaPre} quedando en {sumaTotal} en {tiempoSuma1-tiempoSuma0} en sumar y  {tiempoSuma2-tiempoSuma0} esperado")

    tiempoHilo0 = time.time()
    tiempoHilo1 = time.time()
    print(f"\t{nombre}: he terminado en total en {tiempoHilo1 - tiempoHilo0}")

listaH = []
for i in range(cuantosHilos):
    t = threading.Thread(target=suma,args=["NombreS_" + str(i+1),cuantos,"suma",])
    listaH.append(t)

for i in range(5):
    t = threading.Thread(target=suma,args=["NombreR_" + str(i+1),cuantos,"restado",])
    listaH.append(t)


for s in listaH:
    s.start()

for j in listaH:
    j.join()

print()
print(f"el total sumado por todas los hilos es de : {sumaTotal}")
print()


print("Yasta")