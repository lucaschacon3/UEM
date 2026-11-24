# — Hospital de urgencias
#Lista compartida pacientes = [] con un Lock.

#1 RECEPCIONISTA (productor):
#Añade 8 pacientes a la lista (1 cada 2 segundos)
#Cada paciente es un string tipo "Paciente_1", "Paciente_2"...

#1 MÉDICO (consumidor):
#Revisa la lista cada 1 segundo
#Si hay pacientes, atiende al primero (pop(0)) y tarda 3 segundos en atenderlo (sleep(3))
#Termina cuando ha atendido a 8 pacientes

import threading 
import time

pacientes = []
mutex = threading.Lock()

def recepcionista():
    
    for i in range(8):
        time.sleep(2)
        mutex.acquire()
        pacientes.append("Paciente_"+ str(i+1))
        print(f"PRODUCTOR => {pacientes}")
        mutex.release()

def medico():
    procesando = 0
    while procesando < 8:
            time.sleep(1)
            mutex.acquire()
            atiende = None
            if len(pacientes) > 0:
                atiende= pacientes.pop(0)
                procesando += 1
            mutex.release()
            if atiende is not None:
                print(f"ATENDIENDO : {atiende} ")
                time.sleep(3)
                print(f"PACIENTE ATENDIDO. / nº {atiende} ")


h1 = threading.Thread(target=recepcionista)
h2 = threading.Thread(target=medico)
                                                            

h1.start()
h2.start()

h1.join()
h2.join()


print("TODOS LOS PACIENTES ATENDIDOS...")

