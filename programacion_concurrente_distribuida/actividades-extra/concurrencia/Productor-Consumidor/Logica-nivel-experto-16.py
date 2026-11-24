#Productor–consumidor con bucles infinitos
#➜ Usa while True con time.sleep() para simular que un hilo produce y otro consume (como tu ejemplo anterior).

import random
import time
import threading

mutex = threading.Lock()
buffer = []

#PRODUCTOR 
def productor():
    while True:
        numero = random.randint(1,100)
        acquire = mutex.acquire(timeout=2)

        if acquire:
            buffer.append(numero)
            print(f"PRODUCTO añadimos => {numero} => Añadido al Buffer  =>{buffer}")
            mutex.release()
        else:
            print("PRODUCTOR NO PUEDES  AQUIRIR MUTEX")
        time.sleep(3)


def  consumidor():
    while True:
        acquire = mutex.acquire(timeout=2)
        if acquire:
            if len(buffer) > 0:
                valor = buffer.pop(0)
                print(f"[CONSUMIDOR] consumido =>{valor} => Buffer ahora => {buffer}")
            else:
                print("CONSUMIDOR BUFFER VACIO ")
            mutex.release()
        else:
            print("el consumidor no puede adquirir mutex")
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


