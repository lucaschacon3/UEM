# Tenemos un cine donde el de las taquillas está "más quemado que la pipa de un indio", por lo que ha apagado el walkie para que nadie le moleste mientras vende entradas.

# Por otro lado, a los 3o segundos de empezar a venderse entradas, se declara un incendio en la sala del cine. Y tienen que venir los bomberos a sacar a la gente por dos salidas de emergencia.

# Cada salida de emergencia, puede sacar a dos personas a la vez.

# Hay gente ya en la sala? Si. Puede haber entre 20 y 30 personas, aleatoriamente.

# Cuantas entradas se venden a la vez? Se pueden vender de 1 a 5 entradas en cada venta.

# Cuanto tardamos en vender las entradas? 3 segundos por entrada.

# Aforo de la sala: no revendemos entradas al quemar gente, asi que el aforo tiene que ser fijo (maximo 100 personas)

# Puede salir una persona individual

# Velocidad de salida por la puerta aleatoria entre 10 y 15 segundos

# Hazme el programa siguiendo estas indicaciones

# DINAMICA

import threading
import time
import random

# Parámetros
teamBomberos = 4 # 2 por cada puerta
sala = []
Parking = [[], []]
persona = "P"
aforo = 100
maxAsientos = aforo # Es el numero de asientos que QUEDAN POR VENDER
puerta1 = threading.Semaphore(2)
puerta2 = threading.Semaphore(2)
semaforos = [puerta1, puerta2]

mutex = threading.Lock()

def initSala(maxEntradas, persona):
    global sala
    preventa = random.randint(20, 30)
    print(f"Vamos a inicializar la sala con {preventa} personas ya sentadas en preventa")
    for i in range(preventa):
        sala.append(persona)

        print(f"SALA (PREVENTA)-> {sala}")

    # Descontamos las entradas ya vendidas en preventa
    return maxEntradas - preventa 

def taquillaProductor(persona):
    global sala
    global mutex
    global maxAsientos
    vendido = False
    while maxAsientos > 0: # Vamos descontando a medida que vendemos
        vendido = False
        numPersonasVenta = random.randint(1, 5)
        time.sleep(3 * numPersonasVenta)
        while(not vendido):
            if mutex.acquire(timeout=2):
                for i in range(numPersonasVenta):
                    sala.append(persona)
                    maxAsientos -= numPersonasVenta
                mutex.release()
                print(f"Hemos vendido {numPersonasVenta} entradas. Quedan {maxAsientos} de aforo")
                print(f"SALA->{sala}")
                vendido = True
            else:
                time.sleep(random.randint(1, 3)) # Esperamos un poco antes de volver a intentar
                print(f"Taquilla: no hemos podido vender entradas porque hay un niño enrabietado gritando")

def bomberoConsumidor(puerta, hoja,persona,teamBomberos,aforo):
    # Puerta 1A y 1B -> 0 y 1
    # Puerta 2A y 2B -> 2 y 3
    global semaforos
    global sala
    miSemaforo = semaforos[puerta-1]
    idBombero = 0
    maxPosSalvar = 0
    pos = 0
    rescatada = False
    match str(puerta)+str(hoja):
        case "1A":
            idBombero = 0
        case "1B":
            idBombero = 1
        case "2A":
            idBombero = 2
        case "2B":
            idBombero = 3
        case _:
            idBombero = -1 # Error
            print("Hay un error con el id del bombero")
    maxPosSalvar = aforo-teamBomberos+idBombero-1

    print(f"Soy un bombero, y voy a salvar gente por la puerta {puerta+hoja}")
    while((pos != maxPosSalvar)):
        if (len(sala) > 0):
            while((sala[len(sala)-1] == persona)):
                victima = ""
                if pos <= (len(sala)-1):
                    rescatada = False
                    while ((not rescatada) & (len(sala) != aforo)):
                        if miSemaforo.acquire(timeout=2):
                            victima = sala[pos+idBombero]
                            sala[pos+idBombero] = " "    # La sacamos de la sala
                            miSemaforo.release()
                            rescatada = True
                        else:
                            time.sleep(random.randint(3, 5))
                    time.sleep(random.randint(10, 15))
                    print(f"El bombero {idBombero} en la puerta {puerta}-{hoja} ha salvado a una persona {victima}")
                    pos+=teamBomberos
                else:
                    time.sleep(random.randint(3, 5))
        else:
            time.sleep(random.randint(3, 5))



print(f"El cine abre")
maxAsientos = initSala(maxAsientos, persona)
listaHilos = []
hTaquilla = threading.Thread(target=taquillaProductor, args=[maxAsientos, persona,])
listaHilos.append(hTaquilla)
print(f"FUEGO!!!")
for s in listaHilos:
    s.start()

for j in listaHilos:
    j.join()

print(f"El cine se ha quemado")