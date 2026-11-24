import threading       # Importa el módulo para trabajar con hilos
import time            # Importa funciones relacionadas con el tiempo (sleep, etc.)
import random          # Importa funciones para generar números aleatorios
import math            # Importa funciones matemáticas (ceil, etc.)

# ===========================
# CONFIGURACIÓN DEL PROGRAMA
# ===========================

TIEMPO_MIN = 2         # Tiempo mínimo (en segundos) que duerme cada hilo contador
TIEMPO_MAX = 5         # Tiempo máximo (en segundos) que duerme cada hilo contador

# Lista compartida donde cada posición es el contador de un hilo
lista = []             # Al principio está vacía; se rellena en main()

# Lock (candado) para proteger el acceso a la lista compartida
lock = threading.Lock()  # Solo un hilo a la vez podrá entrar en la sección crítica


def contador(indice, max_valor):
    """
    Función que ejecuta cada hilo contador.
    Cada hilo incrementa su propia posición en la lista
    (lista[indice]) hasta llegar a max_valor.
    """

    # Mientras el valor de mi posición sea menor que el máximo permitido
    while lista[indice] < max_valor:

        # ENTRADA A SECCIÓN CRÍTICA
        lock.acquire()  # Pide el candado; si otro hilo lo tiene, espera

        # Vuelvo a comprobar dentro del lock por seguridad
        if lista[indice] < max_valor:
            # Incremento mi contador en 1
            lista[indice] = lista[indice] + 1

        # SALIDA DE SECCIÓN CRÍTICA
        lock.release()  # Libero el candado para que otros hilos puedan entrar

        # El hilo "descansa" entre TIEMPO_MIN y TIEMPO_MAX segundos
        tiempo_espera = random.randint(TIEMPO_MIN, TIEMPO_MAX)
        time.sleep(tiempo_espera)


def monitor(max_valor, num_hilos):
    """
    Hilo monitor:
    - Lee la lista cada 2 segundos
    - Muestra el estado de la lista
    - Calcula el porcentaje global de progreso
    - Termina cuando se ha llegado al 100%
    """

    # Valor total máximo a alcanzar entre todos los hilos
    # (por ejemplo, si max_valor=10 y num_hilos=3, el total máximo es 30)
    total_maximo = max_valor * num_hilos

    terminado = False  # Bandera para saber cuándo terminar el monitor

    # Mientras el proceso no haya terminado
    while not terminado:

        # ENTRADA A SECCIÓN CRÍTICA (LECTURA SEGURA)
        lock.acquire()       # Pide el candado para leer la lista sin interferencias
        copia = lista[:]     # Hace una copia de la lista para trabajar fuera del lock
        lock.release()       # Libera el candado lo antes posible

        # Suma global de todos los contadores
        suma_total = sum(copia)

        # Cálculo del porcentaje: (suma_total / total_maximo) * 100
        porcentaje = (suma_total * 100) / total_maximo

        # Redondea hacia arriba para no ver decimales
        porcentaje = math.ceil(porcentaje)

        # Muestra la lista y el progreso por pantalla
        print("Lista:", copia)
        print("Progreso:", porcentaje, "%")
        print("-------------------------------")

        # Condición de parada:
        # Si ya hemos alcanzado (o superado) el total máximo, terminamos el monitor
        if suma_total >= total_maximo:
            terminado = True
        else:
            # Si todavía no hemos llegado al total, esperamos 2 segundos
            time.sleep(2)


def main():
    """
    Función principal del programa:
    - Configura el número de hilos y el valor máximo
    - Inicializa la lista compartida
    - Crea e inicia hilos contadores y el hilo monitor
    - Espera a que todos terminen
    """

    num_hilos = 3      # Número de hilos contadores
    max_valor = 10     # Valor máximo que contará cada hilo

    # Inicializamos la lista compartida con tantos ceros como hilos
    # Cada posición de la lista pertenece a un hilo
    for _ in range(num_hilos):
        lista.append(0)

    # Creamos la lista que guardará los objetos Thread de los contadores
    hilos = []

    # Creamos cada hilo contador y lo añadimos a la lista de hilos
    for i in range(num_hilos):
        hilo = threading.Thread(target=contador, args=(i, max_valor))
        hilos.append(hilo)

    # Creamos el hilo monitor, que mostrará el progreso
    hilo_monitor = threading.Thread(target=monitor, args=(max_valor, num_hilos))

    # Iniciamos los hilos contadores
    for h in hilos:
        h.start()

    # Iniciamos el hilo monitor
    hilo_monitor.start()

    # Esperamos a que todos los hilos contadores terminen
    for h in hilos:
        h.join()

    # Esperamos a que el hilo monitor también termine
    hilo_monitor.join()

    # Mensaje final con el resultado
    print("FIN. Resultado final:", lista)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
