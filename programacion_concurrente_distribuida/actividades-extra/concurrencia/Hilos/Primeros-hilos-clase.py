import time
import random
import threading

def cualquiera(nombre):
    for i in range(100):
        print(f"{nombre}: Cualquier cosa")
        time.sleep(4/10)

def otra():
    for i in range(100):
        time.sleep(3/10)
        print("Mas cosas")


print("Hola mundo")
cuantos=int(input("Acho pijo cuantos prosesos\n"))

listaH=[]
for i in range (cuantos):
    t = threading.Thread(target=cualquiera,args=["Hilo_"+str(i+1),])
    listaH.append(t)

for h in listaH:
    h.start()
    
for j in listaH:
    j.join()



print("Adios mundo cruel")