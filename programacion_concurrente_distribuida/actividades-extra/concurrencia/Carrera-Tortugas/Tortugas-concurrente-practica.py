import argparse
import random
import time
import threading
from typing import List, Optional

META = 100.0

# Usamos un único mutex 
mutex = threading.Lock()


class Tortuga(threading.Thread):
    def __init__(self, nombre: str):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.distancia = 0.0
        self.finished = False
        self.tiempo_final: Optional[float] = None
        self.ganadora = False

    def mover(self):
        #Calcula un avance aleatorio
        velocidad = random.uniform(0.5, 3.0)
        delta_t = random.uniform(0.2, 1.5)

        avance = velocidad * delta_t
        self.distancia = self.distancia + avance
        return avance

    def run(self):
        #Cada tortuga corre en su propio hilo
        while self.finished == False:

            avance = self.mover()
            print(f"{self.nombre}: +{avance:.2f} m -> {self.distancia:.2f} m")

            if self.distancia >= META and self.finished == False:
                self.finished = True
                self.tiempo_final = time.time()

                # Intentar marcar ganador usando el mutex
                acquired = mutex.acquire(False)
                if acquired == True:
                    self.ganadora = True
                    print(f"⚡ {self.nombre} CRUZÓ LA META (GANADORA PROVISIONAL)")
                else:
                    print(f"{self.nombre} cruzó la meta")

            time.sleep(0.25)  # pequeña pausa visual


def crear_tortugas(n: int) -> List[Tortuga]:
    lista = []
    contador = 1
    while contador <= n:
        nombre = "Tortuga-" + str(contador)
        lista.append(Tortuga(nombre))
        contador = contador + 1
    return lista


def run_race(n: int = 5, seed: Optional[int] = None):

    if seed is not None:
        random.seed(seed)

    tortugas = crear_tortugas(n)

    print(f"Iniciando carrera con {n} tortugas. Meta = {META} m\n")

    # Lanzar hilos
    i = 0
    while i < len(tortugas):
        tortugas[i].start()
        i = i + 1

    # Esperar que terminen
    j = 0
    while j < len(tortugas):
        tortugas[j].join()
        j = j + 1

    print("\n---> RESULTADOS <---\n")

    # Buscar ganador
    ganadora = None
    k = 0
    while k < len(tortugas):
        if tortugas[k].ganadora == True:
            ganadora = tortugas[k]
        k = k + 1

    if ganadora is not None:
        print(f"GANADORA ABSOLUTA: {ganadora.nombre} con {ganadora.distancia:.2f} m\n")
    else:
        print("Nadie ganó (error inesperado)\n")

    # Ordenar por tiempo de llegada
    tortugas_ordenadas = sorted(
        tortugas,
        key=lambda t: (t.tiempo_final if t.tiempo_final is not None else float('inf'))
    )

    print("Clasificación final:")
    pos = 1
    for t in tortugas_ordenadas:
        tf = "-"
        if t.tiempo_final is not None:
            tf = f"{t.tiempo_final:.3f}"

        print(f"{pos}. {t.nombre} -> {t.distancia:.2f} m  tiempo={tf}")
        pos = pos + 1


def parse_args():
    p = argparse.ArgumentParser(description="Carrera de tortugas con concurrencia => ")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    run_race(n=args.n, seed=args.seed)


if __name__ == "__main__":
    main()