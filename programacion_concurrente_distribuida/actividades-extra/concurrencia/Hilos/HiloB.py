import threading
import time
import random


mutex1 = threading.Lock()
mutex2 = threading.Lock()



def hilo_A():
    print("Hilo b INTENTANDO AQUIRIR MUTEX 2")
    if mutex1.acquire(timeout=2):
            print("Hilo A aquirio Mutex 2")
            time.sleep(3)#simulamos trabajo en mutex 2
            print("Hilo A intentando adquirir Mutex 1")
            if mutex.acquiere(timeout=2):
                print("Hilo B adquirio mUTEX 1")
            #REALIZA EL TRABAJO EN mUTEX 1
                mutex1.release()
            else:
                print("Hilo B no pudo adquiri Mutex 1, liberado")
                mutex2.release()
    else: 
        print("Hilo B no pudo adquirir Mutex 2")






#Funcion para el hilo B

def hilo_B():
    print("Hilo b INTENTANDO AQUIRIR MUTEX 2")
    if mutex2.acquire(timeout=2):
            print("Hilo B aquirio Mutex 2")
            time.sleep(1)#simulamos trabajo en mutex 2
            print("Hilo B intentando adquirir Mutex 1")
            if mutex1.acquiere(timeout=2):
                print("Hilo B adquirio mUTEX 1")
            #REALIZA EL TRABAJO EN mUTEX 1
                mutex1.release()
            else:
                print("Hilo B no pudo adquiri Mutex 1, liberado")
                mutex2.release()
    else: 
        print("Hilo B no pudo adquirir Mutex 2")


