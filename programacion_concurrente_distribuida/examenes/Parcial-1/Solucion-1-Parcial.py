import threading
import time
import random



#Escribe un programa que cuente números en paralelo, de uno en uno, hasta un valor máximo configurable. 
# El programa tendrá una lista en la que, en cada posición, llevará la cuenta de cada uno de los hilos paralelos que 
# realizan el conteo. Cada hilo deberá usar los mecanismos necesarios para acceder a la lista 
# común y poder sumar +1 en la posición de la lista asignada para él. Después de cada suma, 
# cada hilo esperará entre 2 y 5 segundos para volver a sumar, hasta que se llegue al número 
# máximo indicado (2 puntos)

Lista =[0,0,0]
mutex = threading.Lock()

def contar(idHilo,maxVal):

    while Lista[idHilo]< maxVal:

        mutex.acquire()
        Lista[idHilo]+=1         
        mutex.release()
        print(Lista)
        time.sleep(random.randint(2,5))




def main():
     
    max_valor = 10
    hilos= []

    for i in range(len(Lista)):
        hilo = threading.Thread(target = contar, args=(i,max_valor))
        hilos.append(hilo)

    for h  in hilos:
        h.start()
    
    for h in hilos:
        h.join()

    print(f"resultado, {Lista}")

if __name__ == "__main__":
    main()