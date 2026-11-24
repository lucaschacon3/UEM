import time 
import random
import threading


def sumar(nombre,cuantos):
    x = 0
    for i in range(cuantos):
        sPre = x
        x+=1
        print(f"{nombre} : sumamos 1 a {sPre} quedando en {x}")
        time.sleep(random.randint(1,3)/10)
        
hilos = 10
numeroSumar = 100
print(f"Vamos a sumar cosas")
listaH = []

for i in range(hilos):
    t = threading.Thread(target=sumar,args=["nombre"+ str(i+1),numeroSumar])
    listaH.append(t)

lanzar = time.time()
finales = []

for s in listaH:
    s.start()
    lanzando = time.time()
    finales.append(lanzado)

for j in listaH:
    j.join()

x =1 
for e in finales:
    print(f"finales{x} ha tardado en lanzarse ")