#dos funciones de anadir un productos y un consumidor a una lista!
#con hilosimport threading

import threading
import time
import random

# Lista compartida entre productor y consumidor
lista_productos = []

# Cerradura (lock) para proteger el acceso a la lista
lock = threading.Lock()

# ============================================================
# FUNCIÓN: añadir_productos (productor)
# ============================================================
def añadir_productos():
    """
    Añade productos a la lista cada 2 segundos.
    Cada producto es un número aleatorio.
    """
    for i in range(5):
        lock.acquire()
        try:
            producto = random.randint(1, 100)
            print(f"[Productor] Añadiendo producto: {producto}")
            lista_productos.append(producto)
            print(f"[Productor] Lista actual: {lista_productos}")
        finally:
            lock.release()
        time.sleep(2)  # simula el tiempo de producción


# ============================================================
# FUNCIÓN: consumir_productos (consumidor)
# ============================================================
def consumir_productos():
    """
    Elimina productos de la lista cada 3 segundos,
    solo si la lista no está vacía.
    """
    for i in range(5):
        lock.acquire()
        try:
            if len(lista_productos) > 0:
                producto = lista_productos.pop(0)
                print(f"[Consumidor] Consumiendo producto: {producto}")
            else:
                print("[Consumidor] No hay productos disponibles")
            print(f"[Consumidor] Lista actual: {lista_productos}")
        finally:
            lock.release()
        time.sleep(3)  # simula el tiempo de consumo


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
if __name__ == "__main__":
    hilo_productor = threading.Thread(target=añadir_productos)
    hilo_consumidor = threading.Thread(target=consumir_productos)

    # Iniciamos los hilos
    hilo_productor.start()
    hilo_consumidor.start()

    # Esperamos a que ambos terminen
    hilo_productor.join()
    hilo_consumidor.join()

    print("✅ Proceso completado.")
