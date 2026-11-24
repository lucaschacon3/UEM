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

#Dinamica para añadir estatica para sacar
import random
import threading
import time


sala = []
parking = [[],[],[],[]]
persona = "P"
maxAsientos = 100 #es el numero de asientos que quedan por vender 

puerta1 = threading.Semaphore(2)
puerta2 = threading.Semaphore(2)
semaforos = [puerta1,puerta2]
mutex = threading.Lock()

def initSala(maxEntradas,persona):
    global sala
    preventa = random.randint(20,30)
    print("Vamos inicializar la sala con {preventa} las personas sentadas en preventa")
    for i in range(preventa):
        sala.append(persona)
    print(f"sala (PREVENTA) => {sala}")
        #descontamos las entradas vendidas en preventa
    return maxEntradas - preventa 

def taquillaProductor(persona):
    global sala
    global mutex
    global maxEntradas
    vendido = False
    while maxEntradas > 0:#vamos a descontando a medida que vendemos 
        numPersonasVenta = random.randint(1,5)
        time.sleep(3*numPersonasVenta)
        while not vendido:
            if mutex.acquire(timeout=2):
                for i in range(numPersonasVenta):
                    sala.append(persona)
                    maxEntradas -= numPersonasVenta
                mutex.release()
                print(f"hemos vendidos{numPersonasVenta} entradas QUEDAN{maxEntradas} de aforo")
                print(f"SALA => {sala}")
                vendido = True
            else:
                time.sleep(random.randint(1,3))
                print(f"Taquilla => no hemos podidos vender entrada porque hay un niño enrabietado gritando")

def bomberoConsumidor(puerta,hoja):
    global semaforos
    miSemaforos = semaforos[puerta-1]
    print(f"Soy un bomberon, y voy a salvar gente por la puerta{puerta+hoja}")
    while((sala[len(sala)-1 ]== persona) & (maxEntradas>0)):
        

print("cine abre!!")
maxAsientos = initSala(maxAsientos,persona)
listaHilos= []
hTaquilla = threading.Thread(target=taquillaProductor ,args=[maxAsientos,persona])
listaHilos.append(hTaquilla)
print("Fuego!!!!")

for s in  listaHilos:
    s.start()

for j in  listaHilos:
    j.join()  