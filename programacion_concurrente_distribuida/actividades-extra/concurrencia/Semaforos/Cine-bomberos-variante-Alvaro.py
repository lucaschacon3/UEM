import random
import time
import threading

'''
Tenemos un cine donde el de las taquillas está más quemao que la pipa' un indio, por lo que ha apagado el walkie
para que nadie le moleste mientras vende entradas.

Por otro lado, a los 30 segundos de empezar a venderse entradas, se declara un incendio en la sala del cine
y tienen que venir los bomberos a sacar a la gente por dos salidas de emergencia.

Cada salida de emergencia puede sacar a dos personas a la vez.

Hay gente ya en la sala? Sí. Puede haber entre 20 y 30 personas aleatoriamente.

Cuantas entradas se venden a la vez? Se pueden vender de 1 a 5 entradas en cada venta.

Cuanto tardamos en vender las entradas? 3 segundos por entrada.

Aforo de la sala: No revendemos entradas al quemar gente, así que el aforo tiene que ser fijo (max 100 personas).

Puede salir una persona individual.

Velocidad de salida por la puerta aleatoria (entre 10 y 15 segundos)
'''

Sala = []
genteSala = random.randint(20,30)
semaphore = threading.Semaphore(2)
mutex = threading.Lock()

for i in range(genteSala):
     ocupado = "X"
     Sala.append(ocupado)

for j in range(100 - genteSala):
    libre = "0"
    Sala.append(libre)

print("Sala inicial: \n")
print(Sala)

def puertas():
    global Sala
    personasFuera = 0
    conseguido = False
    while not (conseguido):
        if semaphore.acquire():
            while "X" in Sala:
                tiempoEspera = random.randint(10,15)/10
                print(f"Tarda en huír {tiempoEspera} segundos")
                time.sleep(tiempoEspera)

                personasFuera = 0
                for i in range(len(Sala)):
                    if Sala [i] == "X" and personasFuera <= 2:
                        Sala [i] = "0"
                        personasFuera += 1
            print(Sala)
            semaphore.release()
            conseguido = True
        else:
            print("No queda gente en la sala")
    

def ventaEntradas():
    time.sleep(30/10)
    global Sala
    conseguido = False

    while not (conseguido):
        if mutex.acquire():
            while "0" in Sala:
                entradasVendidas = random.randint(1,5)
                tiempoEspera = (entradasVendidas * 3)/10
                print(f"Vende {entradasVendidas} entradas")
                print(f"Tarda en vender las entradas {tiempoEspera} segundos")

                vendidas = 0
                for i in range(len(Sala)):
                    if Sala [i] == "0" and vendidas <= entradasVendidas:
                        Sala [i] = "X"
                        vendidas += 1

                print(Sala)
                
                time.sleep(tiempoEspera)

            conseguido = True

            mutex.release()
        else:
            print("La sala está llena")

listaH = []

for i in range(3):
    puerta1 = threading.Thread(target=puertas)
    puerta2 = threading.Thread(target=puertas)
    vendedor = threading.Thread(target=ventaEntradas)


    listaH.append(puerta1)
    listaH.append(puerta2)
    listaH.append(vendedor)

for s in listaH:
    s.start()

for j in listaH:
    j.join()