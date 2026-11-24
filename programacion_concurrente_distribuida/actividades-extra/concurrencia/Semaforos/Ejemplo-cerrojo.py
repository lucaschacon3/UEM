"""EJEMPLO - CERROJO"""

import threading

#Variable compartida entre hilos
contador = 0 # pylint: disable=invalid-name

#Creacion de un cerrojo para controlar el acceso a la variable compartida
cerrojo = threading.Lock()

#Funcion q los hilos van a ejecutar(acquire y release)
def incrementar():
    """Función que simula el acceso a la variable CONTADOR mediante el cerrojo.
    
    Incrementa el contador 1000 veces, asegurando que solo un hilo pueda 
    acceder a la variable al mismo tiempo utilizando acquire() y release().
    """
    global contador
    for _ in range(1000):
        #se bloquea el acceso a CONTADOR con el cerrojo
        cerrojo.acquire()
        contador += 1
        #se libera el cerrojo pa q otros hilos pueden acceder
        cerrojo.release()

#Funcion q los hilos van a ejecutar(with)
def incrementar_v2():
    """Función alternativa que incrementa CONTADOR usando el cerrojo con 'with'.
    
    Utiliza la declaración 'with' para manejar automáticamente el cerrojo, 
    bloqueando el recurso al entrar en el bloque y liberándolo al salir.
    """
    global contador
    for _ in range(1000):
        with cerrojo: #bloquea el recurso al entrar en el bloque y lo libera al salir
            contador += 1

#Se crea hilos q ejecutan la misma funcion
hilo1 = threading.Thread(target=incrementar, args=())
hilo2 = threading.Thread(target=incrementar, args=())

#Se inicializan los hilos
hilo1.start()
hilo2.start()

#Se espera q cada hilo termine
hilo1.join()
hilo2.join()

#Se muestra el resultado
print("Valor final del contador: ", contador)

# NOTAS:
# El cerrojo actúa como una regla que los hilos deben seguir.
# Primero se bloquea y se adquiere el cerrojo, luego se modifica el recurso,
# y finalmente se libera para que otros hilos puedan continuar su ejecución.
# La versión con 'with' es más segura porque gestiona automáticamente
# el bloqueo y la liberación del cerrojo, evitando problemas si se produce
# una excepción durante la ejecución.
