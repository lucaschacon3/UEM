# EXAMEN 1 PARTE DIGITAL (MEJORADA CON GPT)
import threading  # Para manejar hilos.
from time import sleep  # Para simular pausas en la ejecución.
from random import randint  # Para generar números aleatorios.
import queue  # Para crear una cola segura para hilos.
import math  # Para operaciones matemáticas como redondeo.

# Variables globales
nGallinas = 5  # Número inicial de gallinas.
gallinas = []  # Lista que almacenará los hilos de cada gallina.
huevos = []  # Lista para contar los huevos puestos por cada gallina.
sinHuevos = []  # Lista para contar los días improductivos de cada gallina.
criadero = queue.Queue()  # Cola que almacena huevos fértiles.

# Semáforos para controlar acceso a recursos compartidos.
semaforoHuevo = threading.Semaphore(nGallinas)  # Controla acceso a la lista de huevos.
semaforoSinHuevo = threading.Semaphore(nGallinas)  # Controla acceso a la lista de días improductivos.

pantalla = threading.Lock()  # Candado para asegurar que los mensajes se impriman correctamente.
dias = 0  # Contador global de días.

# Función principal para iniciar la simulación.
def iniciar():
    global nGallinas, gallinas, huevos, sinHuevos

    # Crear los hilos para las gallinas y sus contadores iniciales.
    for i in range(nGallinas):
        gallinas.append(threading.Thread(target=gallina, args=(f"gallina {i+1}", i, 0,)))
        huevos.append(0)  # Cada gallina empieza con 0 huevos puestos.
        sinHuevos.append(0)  # Cada gallina empieza con 0 días improductivos.

    # Crear hilos adicionales para monitoreo y manejo del criadero.
    hiloEstado = threading.Thread(target=estado)  # Monitorea el porcentaje de producción.
    hiloPollitos = threading.Thread(target=pollitos)  # Maneja huevos fértiles y nuevas gallinas.

    # Iniciar todos los hilos de gallinas y los hilos adicionales.
    for x in gallinas:
        x.start()
    hiloEstado.start()
    hiloPollitos.start()

    # Esperar a que todos los hilos terminen su ejecución.
    for x in gallinas:
        x.join()
    hiloEstado.join()
    hiloPollitos.join()

# Función que simula el comportamiento de una gallina.
def gallina(name, pos, dia):
    global nGallinas, gallinas, huevos, sinHuevos, criadero

    # Cada gallina simula un año (365 días).
    while dia != 365:
        posibilidadHuevo = randint(1, 300) / 365  # Probabilidad de poner un huevo.
        puesto = False  # Bandera para saber si la gallina ya "resolvió" el día.

        if posibilidadHuevo > 0.18:  # Si la probabilidad es suficiente para poner un huevo.
            posibilidadCriadero = randint(1, 100) / 100  # Probabilidad de que el huevo sea fértil.

            if posibilidadCriadero > 0.02:  # Si el huevo no es fértil.
                while not puesto:
                    if semaforoHuevo.acquire(timeout=2):  # Intenta acceder a la lista de huevos.
                        huevos[pos] += 1  # Incrementa el contador de huevos para esta gallina.
                        puesto = True  # Marca que el día ya se resolvió.
                        semaforoHuevo.release()  # Libera el semáforo.

                        # Imprime un mensaje indicando que puso un huevo.
                        if pantalla.acquire():
                            print(f"{name}, he puesto huevo")
                            pantalla.release()
            else:  # Si el huevo es fértil, se agrega al criadero.
                criadero.put(0)  # Un huevo fértil comienza con valor 0.

                if pantalla.acquire():
                    print(f"{name}, mi huevo es fertil")
                    pantalla.release()
        else:  # Si no pone un huevo.
            while not puesto:
                if semaforoSinHuevo.acquire(timeout=2):  # Intenta acceder a la lista de días improductivos.
                    sinHuevos[pos] += 1  # Incrementa el contador de días improductivos para esta gallina.
                    puesto = True  # Marca que el día ya se resolvió.
                    semaforoSinHuevo.release()  # Libera el semáforo.

                    # Imprime un mensaje indicando que no puso huevo.
                    if pantalla.acquire():
                        print(f"{name}, no he puesto huevo")
                        pantalla.release()

        dia += 1  # Incrementa el día.
        sleep(randint(1, 3))  # Espera entre 1 y 3 segundos para simular el paso del día.

# Función que maneja el criadero y nuevas gallinas.
def pollitos():
    global criadero, gallinas, nGallinas, huevos, sinHuevos, pantalla, semaforoHuevo, semaforoSinHuevo, dias

    while dias != 365:  # Simula el paso de un año.
        sleep(2)  # Espera 2 segundos antes de procesar el criadero.

        if not criadero.empty():  # Si hay huevos fértiles en el criadero.
            size = len(list(criadero.queue))  # Determina el tamaño actual del criadero.

            for x in range(size):
                huevoCriadero = criadero.get()  # Obtiene un huevo del criadero.

                if huevoCriadero != 140:  # Si el huevo aún no "nace".
                    huevoCriadero += 1  # Incrementa su valor.
                    criadero.put(huevoCriadero)  # Lo regresa al criadero.
                else:  # Si el huevo alcanza el valor 140, nace una nueva gallina.
                    if pantalla.acquire():
                        print("Criadero detiene produccion para añadir nueva gallina")
                        pantalla.release()

                    # Crea un nuevo hilo para la nueva gallina.
                    gallinas.append(threading.Thread(target=gallina, args=(f"gallina {nGallinas+1}", nGallinas, dias,)))
                    huevos.append(0)  # Agrega contadores para la nueva gallina.
                    sinHuevos.append(0)
                    gallinas[nGallinas].start()  # Inicia el hilo de la nueva gallina.
                    nGallinas += 1  # Incrementa el número total de gallinas.

        dias += 1  # Incrementa el contador global de días.

# Función que monitorea el porcentaje de huevos producidos.
def estado():
    global huevos, sinHuevos, criadero

    while dias != 365:  # Simula el paso de un año.
        sleep(2)  # Espera 2 segundos antes de calcular el estado.

        sum = 0
        for x in huevos:  # Suma todos los huevos puestos.
            sum += x

        # Calcula el porcentaje de huevos producidos respecto al máximo teórico.
        porcentaje = (sum / (len(huevos) * 300)) * 100
        porcentaje = math.ceil(porcentaje)  # Redondea hacia arriba.

        if pantalla.acquire():
            print(f"Porcentaje de huevos producidos: {porcentaje}%")
            pantalla.release()

# Ejecuta la simulación.
iniciar()

# Imprime el resumen final.
print("Terminado")  # Indica que la simulación ha finalizado.
sum = 0             # Variable para almacenar la suma total de huevos.

# Suma todos los huevos puestos por las gallinas.
for x in huevos:
    sum += x

# Calcula el porcentaje de producción total respecto al máximo teórico.
porcentaje = (sum / (len(huevos) * 300)) * 100


# Imprime un resumen con el porcentaje de producción, huevos puestos por cada gallina,
# días improductivos de cada gallina y el estado del criadero.
print(f"Porcentaje de huevos producidos: {porcentaje}%, Huevos de cada gallina: {huevos}, Dias improductivos de cada gallina: {sinHuevos}, Criadero: {criadero}")
