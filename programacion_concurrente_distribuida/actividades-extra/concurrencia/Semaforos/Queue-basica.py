import queue

cola = queue.Queue()

cola.put("Hola")

sacado = cola.get()

#n hilos para n prouctoes q van a meter cosas en la cola
#otro hilo para sacar cosas de la cola
#aparte de los 2 anteriores hilos q ya habian hecho anteriormnte 
#basicamnete lo q se hizo con la lista pero ahora con cola