import time
import random
import threading

sumaTotal = 0
cuantos = 100
cuantosHilos = 10
resultadosHilos =[]

mutex= threading.Lock()



def suma(nombre,cuantos,operador):
    global sumaTotal
    global resultadosHilos
    tiempoHilo0= time.time()
    tiempoSuma0=0
    tiempoSuma1=0
    tiempoSuma2=0
    sumaLocal = 0
    for i in range(cuantos):
        sumaPre = sumaTotal
        tiempoSuma0 =  time.time()
        
        if mutex.acquire():
            if operador == "sumado":
                sumaTotal +=1
            elif operador =="restado":
                sumaTotal -=1
            else:
                print("Mal llamado sin 'suma' ni 'resta'")
            sumaLocal = sumaTotal
            mutex.release()
        tiempoSuma1 = time.time()
        tiempoEspera = random.randint(1,3)/10
        tiempoSuma2 = time.time()
        time.sleep(tiempoEspera)
        print(f"{nombre}: ha {operador} 1 {sumaPre} quedando en {sumaLocal} en {tiempoSuma1-tiempoSuma0} en sumar y {tiempoSuma2-tiempoSuma0} esperado")
            
        
    
    tiempoHilo1= time.time()
    # print(f"\t{nombre}: he terminado en total en {tiempoHilo1 - tiempoHilo0}")
    sumaPre +1
    resultadosHilos.append(f"{nombre} ha sumado {sumaPre} en {tiempoHilo1 - tiempoHilo0}")


tiempoTotal0 = time.time()
listaH = []
for i in range(cuantosHilos):
    t= threading.Thread(target=suma,args=["NombreS_"+str(i+1),cuantos,"sumado",])
    listaH.append(t)

for i in range(5):
    t= threading.Thread(target=suma,args=["NombreR_"+str(i+1),cuantos,"restado",])
    listaH.append(t)

for s in listaH:
    s.start()

for j in listaH:
    j.join()
tiempoTotal1 = time.time()

print()
print(f"El total sumado por todos los hilos es de: {sumaTotal} en {tiempoTotal1-tiempoTotal0} segundos ")
print()

for p in resultadosHilos:
    print(p)






print("Yasta!!!")