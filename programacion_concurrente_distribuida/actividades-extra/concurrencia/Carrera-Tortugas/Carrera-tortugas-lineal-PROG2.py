import random
import time


tortugas = {
    "tortuga_1": 0,
    "tortuga_2": 0,
    "tortuga_3": 0,
    "tortuga_4": 0
}

meta = 100
ganador = None
carrera_en_curso = True  

while carrera_en_curso:
    for nombre in tortugas:
        avance = random.randint(1, 10)
        tortugas[nombre] += avance
        print(nombre + " lleva " + str(tortugas[nombre]) + " metros")
        time.sleep(0.2)  

        if tortugas[nombre] >= meta and ganador is None:
            ganador = nombre
            carrera_en_curso = False  
            print("\n " + ganador + " ha ganado la carrera\n")
    
print("La carrera ha terminado")
