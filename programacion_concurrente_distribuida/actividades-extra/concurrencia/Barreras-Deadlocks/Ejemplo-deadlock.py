"""
EJEMPLO - DEAD LOCK

Este código demuestra cómo puede producirse un deadlock (bloqueo permanente) 
en un programa multihilo en Python cuando dos o más hilos intentan adquirir 
recursos compartidos en un orden que puede llevar al bloqueo.

Se definen dos versiones de funciones para ilustrar cómo ocurre el deadlock 
y una posible solución mediante el uso de un tiempo de espera (timeout) 
para evitar que los hilos se queden bloqueados indefinidamente.

"""

import threading
import time

#Recursos compartidos por hilos
recurso1 = threading.Lock()
recurso2 = threading.Lock()

#Funcion para el primer hilo, que simula una posible situación de deadlock
def hilo_a():
    """ Funcion que representa el primer hilo, intenta adquirir recurso 1 y luego recurso 2.
    
    Si el hilo A adquiere recurso1 pero no puede adquirir recurso2 (porque ya lo tiene otro hilo),
    el hilo se bloquea, esperando indefinidamente a que recurso2 esté disponible.
    """
    with recurso1: #adquiere el recurso 1
        print("Hilo A ha adquirido recurso 1")
        time.sleep(1) #simula tiempo de trabajo mientras tiene recurso1
        with recurso2: #intetna adquirir el recurso 2
            print("Hilo A ha adquirido recurso 2")

#Funcion para el segundo hilo, que también simula una posible situación de deadlock
def hilo_b():
    """ Funcion que representa el segundo hilo, intenta adquirir recurso 2 y luego recurso 1.
    
    Si el hilo B adquiere recurso2 pero no puede adquirir recurso1 (porque ya lo tiene otro hilo),
    el hilo se bloquea, esperando indefinidamente a que recurso1 esté disponible.
    """
    with recurso2: #adquiere el recurso 2
        print("Hilo B ha adquirido recurso 2")
        time.sleep(1) #simula tiempo de trabajo mientras tiene recurso 2
        with recurso1: #intenta adquirir el recurso 1
            print("Hilo B ha adquirido recurso 1")


#Solución para evitar el deadlock mediante el uso de un tiempo de espera
def hilo_x():
    """ Funcion alternativa al hilo A que implementa un timeout para evitar el deadlock.
    
    Intenta adquirir recurso1 y, luego, recurso2. Si no logra adquirir el segundo recurso
    en un tiempo determinado, libera el recurso ya adquirido para evitar el bloqueo.
    """
    if recurso1.acquire(timeout=1):  #intenta adquirir recurso1 con límite de tiempo
        print("Hilo A ha adquirido recurso 1")
        time.sleep(1)  #simula trabajo mientras tiene recurso1
        if recurso2.acquire(timeout=1):  #intenta adquirir recurso2 con límite de tiempo
            print("Hilo A ha adquirido recurso 2")
            recurso2.release()  #libera recurso2 si lo adquirió
        recurso1.release()  #libera recurso1 al finalizar

def hilo_y():
    """ Funcion alternativa al hilo B que implementa un timeout para evitar el deadlock.
    
    Intenta adquirir recurso2 y luego recurso1. Si no logra adquirir el segundo recurso
    en un tiempo determinado, libera el recurso ya adquirido para evitar el bloqueo.
    """
    if recurso2.acquire(timeout=1):  #intenta adquirir recurso2 con límite de tiempo
        print("Hilo B ha adquirido recurso 2")
        time.sleep(1)  #simula trabajo mientras tiene recurso2
        if recurso1.acquire(timeout=1):  #intenta adquirir recurso1 con límite de tiempo
            print("Hilo B ha adquirido recurso 1")
            recurso1.release()  #libera recurso1 si lo adquirió
        recurso2.release()  #libera recurso2 al finalizar

#Creacion de hilos que simulan el deadlock
hilo_a = threading.Thread(target=hilo_a, args=())
hilo_b = threading.Thread(target=hilo_b, args=())

#Inician los hilos para demostrar el deadlock
hilo_a.start()
hilo_b.start()

#Espera a que ambos hilos terminen
hilo_a.join()
hilo_b.join()


# NOTAS:
# Un deadlock ocurre cuando dos o más hilos esperan indefinidamente
# que otro hilo libere un recurso que necesitan para continuar.
# En este ejemplo, el deadlock se produce porque el hilo A necesita recurso2 y el hilo B necesita recurso1.
# Ambos hilos quedan bloqueados esperando un recurso que está en uso por el otro hilo.
# Para evitar el deadlock, puede utilizarse un timeout al adquirir recursos
# o asegurar que los recursos se adquieran en el mismo orden en ambos hilos.
