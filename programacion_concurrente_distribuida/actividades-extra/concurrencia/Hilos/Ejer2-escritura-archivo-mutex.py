import threading # permite creacion de hilos y realizar tareas a la vez (concurrencia)
import random
import time # permite hacer pausas en la ejecucion de programa

path = r"D:\Usuario marbe\Desktop\UEM\3er CURSO\PROGRAMACIÓN CONCURRENTE Y DISTRIBUIDA\PROYECT PYTHON\Archivo.txt"

f = open(path, "+a")

f.writelines("Escribiendo archivo\n");

mutex = threading.Lock();

#Funcion para agregar contenido
def escribir():
    f = open(path, "a+") # abre el archivo en modo añadir "a" , sino existe se crea, el "+" permite lectura y escritura
    time.sleep(random.randint(1,5)) # el hilo se "duerme" , simulando asi la variabilidad en el tiempo de ejecucion de los hilos
    f.writelines("\nHilo " + threading.current_thread().name + "\n")
    f.close()

threads = [] # lista vacia para guardar los objetos hilos q se crearán

#Bucle pa' crear hilos (se ejecuta 5 veces en este caso)
for i in range(5):
    threads.append(threading.Thread(target=escribir)) 

#Bucle pa' iniciar cada hilo en la lista utilizando el metodo start()
for s in threads:
    s.start()

# Bucle pa' esperar q cada hilo termine su ejecucion utilizando el metodo join()
for j in threads:
    j.join()