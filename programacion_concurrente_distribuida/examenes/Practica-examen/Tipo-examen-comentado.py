# ---------------------------------------------------------------
# SIMULACIÓN DE UN CINE CON TAQUILLA (PRODUCTOR) Y BOMBEROS (CONSUMIDORES)
# USANDO HILOS, MUTEX Y SEMÁFOROS
# ---------------------------------------------------------------

import threading      # Para crear y manejar hilos
import time           # Para simular tiempos con sleep()
import random         # Para generar valores aleatorios


# ---------------------------------------------------------------
# PARÁMETROS GLOBALES
# ---------------------------------------------------------------

teamBomberos = 4      # Total de bomberos (4) -> 2 por cada puerta
sala = []             # Lista que representa personas ("P") sentadas en la sala
Parking = [[], []]    # No se usa en este programa
persona = "P"         # Símbolo que representa una persona
aforo = 100           # Aforo total del cine
maxAsientos = aforo   # Asientos disponibles para venta (va disminuyendo)

# Semáforos: cada puerta tiene capacidad para 2 bomberos simultáneos
puerta1 = threading.Semaphore(2)
puerta2 = threading.Semaphore(2)
semaforos = [puerta1, puerta2]   # Lista para acceder por índice

# Mutex para proteger acceso simultáneo a sala y maxAsientos
mutex = threading.Lock()


# ---------------------------------------------------------------
# FUNCIÓN PARA INICIALIZAR LA SALA CON ENTRE 20 Y 30 PERSONAS
# ---------------------------------------------------------------

def initSala(maxEntradas, persona):
    global sala
    preventa = random.randint(20, 30)   # Personas ya dentro antes del incendio

    print(f"Vamos a inicializar la sala con {preventa} personas ya sentadas en preventa")

    # Añadimos cada persona a la sala
    for i in range(preventa):
        sala.append(persona)
        print(f"SALA (PREVENTA)-> {sala}")   # Mostrar estado actual de la sala

    # Restamos del aforo las entradas ya ocupadas
    return maxEntradas - preventa 


# ---------------------------------------------------------------
# TAQUILLA (PRODUCTOR)
# VENDE ENTRADAS ENTRE 1 Y 5 POR OPERACIÓN
# TARDANDO 3 SEGUNDOS POR PERSONA
# ---------------------------------------------------------------

def taquillaProductor(persona):
    global sala
    global mutex
    global maxAsientos

    vendido = False

    # Mientras queden asientos por vender
    while maxAsientos > 0:

        vendido = False
        numPersonasVenta = random.randint(1, 5)   # Entradas que queremos vender

        # Tiempo total de venta = personas * 3 segundos
        time.sleep(3 * numPersonasVenta)

        # Intentamos vender (necesitamos el mutex para entrar en sección crítica)
        while(not vendido):

            # Intentamos obtener el lock durante máximo 2 segundos
            if mutex.acquire(timeout=2):

                # Sección crítica: modificamos sala y maxAsientos
                for i in range(numPersonasVenta):
                    sala.append(persona)
                    maxAsientos -= numPersonasVenta   # ❌ ERROR del profesor (debería ser -1)

                mutex.release()   # Liberamos el mutex

                print(f"Hemos vendido {numPersonasVenta} entradas. Quedan {maxAsientos} de aforo")
                print(f"SALA->{sala}")

                vendido = True   # Venta completada

            else:
                # No se pudo obtener el lock (otro hilo lo está usando)
                time.sleep(random.randint(1, 3))
                print("Taquilla: no hemos podido vender entradas porque hay un niño enrabietado gritando")


# ---------------------------------------------------------------
# BOMBERO (CONSUMIDOR)
# SACA PERSONAS DE LA SALA USANDO SEMÁFOROS EN CADA PUERTA
# ---------------------------------------------------------------

def bomberoConsumidor(puerta, hoja, persona, teamBomberos, aforo):

    global semaforos
    global sala

    # Seleccionamos el semáforo correcto según puerta
    miSemaforo = semaforos[puerta-1]

    idBombero = 0
    maxPosSalvar = 0
    pos = 0
    rescatada = False

    # Asignamos ID al bombero según puerta y hoja
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
            idBombero = -1
            print("Hay un error con el id del bombero")

    # Cálculo de la última posición que intentará salvar
    maxPosSalvar = aforo - teamBomberos + idBombero - 1

    print(f"Soy un bombero, y voy a salvar gente por la puerta {puerta+hoja}")

    # Mientras no lleguemos a la posición límite asignada a este bombero
    while(pos != maxPosSalvar):

        # Si hay gente dentro
        if len(sala) > 0:

            # Mientras la última persona sea "P"
            while(sala[len(sala)-1] == persona):

                if pos <= (len(sala)-1):
                    rescatada = False

                    # Mientras no hayamos rescatado a esa persona
                    while((not rescatada) & (len(sala) != aforo)):

                        # Entrar por la puerta → máx 2 bomberos por puerta
                        if miSemaforo.acquire(timeout=2):

                            # Seleccionamos la persona a rescatar
                            victima = sala[pos + idBombero]

                            # Marcamos que la persona ya no está
                            sala[pos + idBombero] = " "

                            miSemaforo.release()
                            rescatada = True

                        else:
                            # Si no se puede usar la puerta, esperamos un poco
                            time.sleep(random.randint(3, 5))

                    # Tiempo de rescate entre 10 y 15 segundos
                    time.sleep(random.randint(10, 15))

                    print(f"El bombero {idBombero} en la puerta {puerta}-{hoja} ha salvado a una persona {victima}")

                    # Avanza posiciones para repartir tareas entre bomberos
                    pos += teamBomberos

                else:
                    time.sleep(random.randint(3, 5))

        else:
            # Si la sala está vacía, esperamos
            time.sleep(random.randint(3, 5))


# ---------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------

print("El cine abre")

# Inicializamos sala (20-30 personas)
maxAsientos = initSala(maxAsientos, persona)

listaHilos = []

# Creamos el hilo de la taquilla
# ⚠️ ERROR: se pasan 2 parámetros pero la función solo usa 'persona'
hTaquilla = threading.Thread(target=taquillaProductor, args=[maxAsientos, persona])
listaHilos.append(hTaquilla)

print("FUEGO!!!")

# Iniciamos hilos
for s in listaHilos:
    s.start()

# Esperamos a que terminen
for j in listaHilos:
    j.join()

print("El cine se ha quemado")
