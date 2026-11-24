
# En este ejemplo, los hilos ejecutan la función imprimir_mensaje de manera concurrente.


import threading #para realizar tareas concurrentes utilizando multiples hilos
import time #para pausar la ejecucion del hilo por intervalos de tiempo
'''
#funcion para imprimir un mensaje 5 veces con pausas de 1 seg entre cada impresion
def imprimir_mensaje(nombre):
    for i in range(5):
        time.sleep(1) #pausa de 1 seg para simular lo q tarda la ejecucion de una tarea
        print("Hola " + nombre + " este es el mensaje" , i)

#creacione o instancias de hilos para ejecutar la funcion "imprimir_mensaje" pero con diferentes argumentos
hilo1 = threading.Thread(target=imprimir_mensaje, args=("Jose",))
hilo2 = threading.Thread(target=imprimir_mensaje, args=("Santi",))

#se inicia la ejecucion de ambos hilos de manera concurrente e independiente
hilo1.start()
hilo2.start()

#asegura q el programa principal espere hasta q cada hilo haya terminado su ejecucion
hilo1.join()
hilo2.join()
'''

# Crea un programa que inicie dos hilos. Uno debe contar del 1 al 5 con una pausa de 1 segundo entre números, 
# y el otro debe imprimir un mensaje de saludo cada 2 segundos, ambos hilos deben correr al mismo tiempo.

def contar_numeros():
    for i in range(5):
        time.sleep(1)
        print("Numero " , i+1)

def imprimir_msj(name):
    for i in range(5):
        time.sleep(2)
        print("Saludo para " + name , i)

hilo1 = threading.Thread(target=contar_numeros, args=())
hilo2 = threading.Thread(target=imprimir_msj, args=("Fernando",))

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()


