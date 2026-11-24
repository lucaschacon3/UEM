import threading
import random
import time



# aleatorio para gener X tortugas
# aleatorio para generar Y velocidad y un Z distancia

# muestra los metros de recorrido de cada totuga
# el movimiento aleatorio terminara hasta q se llegue o supere la Z de 100 metros , distancia de met

# se muestra la tortuga que ganado o llegado a la meta

# el programa esperara a q todos los hilos osea procesos terminen antes de cerrarse o terminar 



def mover_tortugas():
    num = 0;
    i=0
    while i<100:

        vel = random.randint(5,20)
        i = i + random.randint(20, 50)
        num += 1

        time.sleep(0.3);

        print("\nTortuga " , num, ": ")
        print("Velocidad: " , vel)
        print("Distancia: " , i)

    print("La Torguga " , num,  " gano la carrera")

#tort1 = mover_tortugas();
#tort2 = mover_tortugas();
#tort3 = mover_tortugas();


tort1 = threading.Thread(target=mover_tortugas)
tort2 = threading.Thread(target=mover_tortugas)
tort1.start()
tort2.start()
tort1.join()
tort2.join()
