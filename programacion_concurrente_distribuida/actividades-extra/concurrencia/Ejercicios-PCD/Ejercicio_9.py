#Crea un programa con:
# Una lista compartida clientes = [] con un Lock.
# Un contador GLOBAL clientes_atendidos = 0 (compartido por las 2 cajeras).
# 1 hilo ENTRADA (productor):

#Añade 10 clientes a la lista (1 cada 1 segundo)
#Los clientes se llaman "Cliente_1", "Cliente_2", ..., "Cliente_10"
#Imprime cuando entra cada cliente

# 2 hilos CAJERAS (consumidores):
#Cada cajera recibe su nombre por parámetro ("Caja_1" y "Caja_2")
#Revisa la lista cada 0.5 segundos

#Si hay clientes → saca el primero con pop(0) y lo atiende
#"Atender" = time.sleep(random.randint(1, 3)) (entre 1 y 3 segundos aleatorio)
#Imprime cuando empieza y cuando termina de atender a cada cliente
#Las 2 cajeras juntas atienden a los 10 clientes (NO 10 cada una)
#El programa principal:

#Crea los 3 hilos (1 entrada + 2 cajeras)
#start() y join()
#Imprime "SUPERMERCADO CERRADO" al final

import threading 
import time 

clientes = []
clientes_atendidos = 0
mutex = threading.Lock()

def productor():
    global clientes_atendidos
    for i in range(10):
        time.sleep(1)
        mutex.acquire()
        clientes.append("Cliente_" + str(i+1))
        print(f" PRODUCTOR {clientes}  ")

        


