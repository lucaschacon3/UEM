#Productor–consumidor con bucles infinitos
#➜ Usa while True con time.sleep() para simular que un hilo produce y otro consume (como tu ejemplo anterior).

import threading
import random
import time

mutex = threading.Lock()

buffer = []#lista compartida con productor y consumidor

def productor():
    while True:
    #me genera un numero del 1 al 100
            numero = random.randint(1,100)
#Intenta acquirir el mutex con timeout 1seg
            acquire = mutex.acquire(timeout=20)

            if acquire:
                buffer.append(numero)
                print(f"[productor] añadido {numero} => Buffer ahora => {buffer}")
                mutex.release()
            else:
                print("[PRODUCTOR]no pode adquirir mutex")
                
            time.sleep(2)#pausamos el productor

def consumidor():
     
     while True:
          acquire = mutex.acquire(timeout=20)
          
          if acquire:
               if len(buffer)>0:
                    valor = buffer.pop(0)
                    print(f"[consumidor] Consumido {valor} => Buffer ahora => {buffer}")
               else:
                    print("CONSUMIDOR BUFFER VACIO ")
               mutex.release()
          else:
               print("El consumidor no puede acquirir mutex")
          time.sleep(3)

def main():
     
    h1 = threading.Thread(target=productor)
    h2 = threading.Thread(target=consumidor)

    h1.start()
    h2.start()

    h1.join()
    h2.join()


if __name__ == "__main__":
    main()