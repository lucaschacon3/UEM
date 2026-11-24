import threading
import random
import time

def mover_Tortuga():
    i = 0
    while i < 100:
        i += random.randint(0,10)
        print(threading.current_thread().name + " lleva " + str(i) + " metros")
    time.sleep(0.2)
    if(threading.active_count() == 5):
        print(threading.current_thread().name + " ha ganado!")
    else:
        print(threading.current_thread().name + " ha terminado")


tortuga_1 = threading.Thread(target=mover_Tortuga, name="tortuga_1")
tortuga_2 = threading.Thread(target=mover_Tortuga, name="tortuga_2")
tortuga_3 = threading.Thread(target=mover_Tortuga, name="tortuga_3")
tortuga_4 = threading.Thread(target=mover_Tortuga, name="tortuga_4")

tortuga_1.start()
tortuga_2.start()
tortuga_3.start()
tortuga_4.start()
tortuga_1.join()
tortuga_2.join()
tortuga_3.join()
tortuga_4.join()


