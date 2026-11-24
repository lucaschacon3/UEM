"""Imagina una taquilla de cine que vende entradas para una película. 
Los clientes (hilos) llegan y desean comprar boletos, pero solo hay 
un número limitado de boletos disponibles. Utiliza un mutex (cerradura) 
para sincronizar la compra de boletos y asegurarte de que no se vendan 
más boletos de los disponibles
"""
import threading
import time
import random

#Variables globales
TOTAL_BOLETOS = 7  #numero total de boletos disponibles
mutex = threading.Lock()  #mutex para proteger el acceso a los boletos
semaforo = threading.Semaphore(0)  #semaforo para controlar el acceso a los boletos

def comprar_boleto(cliente_id, pudo_comprar):
    global TOTAL_BOLETOS
    #Se intenta comprar un boleto
    mutex.acquire()  #adquiere el mutex para acceso seguro
    if TOTAL_BOLETOS > 0:
        time.sleep(random.uniform(0.1, 0.5))  #simula el tiempo de compra
        TOTAL_BOLETOS -= 1
        print("Cliente ", cliente_id, " ha comprado un boleto. Quedan ", TOTAL_BOLETOS, " boletos.")
        pudo_comprar[0] = True  #actualiza el estado de compra a True
        semaforo.release()  #libera el semáforo para indicar que un boleto fue comprado
    else:
        print("Cliente ", cliente_id, " no pudo comprar un boleto. No quedan boletos disponibles.")
        pudo_comprar[0] = False  #actualiza el estado de compra a False
    mutex.release()  #libera el mutex después de la compra

def cliente(cliente_id, pudo_comprar):
    sigue_intentando = True  #variable para controlar el bucle
    while sigue_intentando:  #para mantener el bucle indefinidamente
        time.sleep(random.uniform(0.1, 1))  #espera aleatoria antes de intentar comprar
        comprar_boleto(cliente_id, pudo_comprar)

        #Verifica si pudo comprar un boleto
        if pudo_comprar[0]:  #si pudo comprar, se cambia la variable para salir del bucle
            sigue_intentando = False  #cambia la variable a False para salir del bucle
        elif TOTAL_BOLETOS <= 0:  #verifica si no quedan boletos
            sigue_intentando = False  #sale del bucle si no quedan boletos

CANT_CLIENTES = 15  #numero de clientes

#Crea y lanza hilos de clientes
clientes = []
pudo_comprar_list = []  #lista para almacenar el estado de compra de cada cliente

for i in range(CANT_CLIENTES):
    pudo_comprar = [False]  #usamos una lista para poder modificarla dentro del hilo
    hilo_cliente = threading.Thread(target=cliente, args=(i + 1, pudo_comprar))
    hilo_cliente.start()
    clientes.append((hilo_cliente, pudo_comprar))  #guarda hilo y estado de compra

#Espera a que todos los hilos terminen
for hilo, _ in clientes:
    hilo.join()

#Salida final organizada
print("\n=========================")
print("   Resumen de compras")
print("=========================")
print("Total de boletos vendidos: ", 7 - TOTAL_BOLETOS)
print("Boletos restantes: ", TOTAL_BOLETOS)
print("Todos los clientes han intentado comprar boletos.")
