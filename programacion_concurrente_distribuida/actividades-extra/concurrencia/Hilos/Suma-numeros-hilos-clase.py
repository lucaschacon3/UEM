import threading
import random
import time

sumaTotal = 0
def sumar(nombre,cuantos):
    global sumaTotal
    x =0
    for i in range(cuantos):
        xPre = sumaTotal
        sumaTotal= sumaTotal + 1
        espera = random.randint(1,3)/100
        time.sleep(espera)
        print(f"{nombre}: sumamos 1 a {xPre} quedando en {sumaTotal} esperando {espera}")
        
        
    sumaTotal += x

hilos = 10
numerosSumar = 100
print(f"Vamos a sumar cosas")
listaH = []
for i in range(hilos):
    t = threading.Thread(target = sumar,args=["nombre_"+str(i+1),numerosSumar,])
    listaH.append(t)

lanzar= time.time()
finales=[]
for s in listaH:
    s.start()
    lanzado = time.time()
    finales.append(lanzado)


for j in listaH:
    j.join()


x = 1
for e in finales:
    print(f"El hilo {x} ha tardado en lanzarse {lanzar-e}")
    x+=1
print(f"La suma total es de {sumaTotal}")
print("Sacabó")