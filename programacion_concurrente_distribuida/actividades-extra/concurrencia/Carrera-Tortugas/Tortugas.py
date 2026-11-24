#!/usr/bin/env python3
"""
Simulador: Carreras de las tortugas (versión lineal)

Uso:
    python tortugas.py [--n N] [--seed S]

Opciones:
    --n N     Número de tortugas (por defecto 5)
    --seed S  Semilla aleatoria para reproducibilidad (opcional)

Descripción:
    Este script crea N tortugas que avanzan de forma aleatoria en cada
    iteración. Cada tortuga genera una velocidad aleatoria (m/s) y un
    tiempo de paso (s) para calcular el avance en metros. La carrera
    termina cuando todas las tortugas han cruzado la meta (100 m). El
    primer cruce se anuncia como ganador, pero el programa espera a que
    todas terminen antes de salir.
"""

import argparse
import random
import time
from typing import List, Optional

META_METROS = 100.0

class Tortuga:
    """Clase que representa una tortuga en la carrera."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.distancia = 0.0
        self.finished = False
        self.tiempo_finished: Optional[float] = None

    def mover(self) -> float:
        """Genera una velocidad y tiempo de paso aleatorios y avanza.

        Retorna la distancia añadida en este paso.
        """
        if self.finished:
            return 0.0

        # velocidad en m/s entre 0.5 y 3.0 (puede ajustar)
        velocidad = random.uniform(0.5, 3.0)
        # tiempo de paso en segundos entre 0.2 y 1.5
        delta_t = random.uniform(0.2, 1.5)
        avance = velocidad * delta_t
        self.distancia += avance

        if self.distancia >= META_METROS:
            self.finished = True
            # Guardamos un timestamp relativo usando time.time()
            self.tiempo_finished = time.time()

        return avance

def crear_tortugas(n: int) -> List[Tortuga]:
    return [Tortuga(f"Tortuga-{i+1}") for i in range(n)]


def run_race(n: int = 5, seed: Optional[int] = None, delay: float = 0.0):
    """Ejecuta la simulación hasta que todas las tortugas terminen.
    Parámetros:
        n: número de tortugas
        seed: semilla para el generador aleatorio (None = aleatorio)
        delay: tiempo en segundos a esperar entre iteraciones (sólo para
            hacer la salida legible; 0 por defecto)
    """
    if seed is not None:
        random.seed(seed)

    tortugas = crear_tortugas(n)
    ganador: Optional[Tortuga] = None
    iteracion = 0

    print(f"Iniciando carrera con {n} tortugas. Meta = {META_METROS} m")

    # Bucle principal: seguimos hasta que todas hayan terminado
    while not all(t.finished for t in tortugas):
        iteracion += 1
        print(f"\n--- Iteración {iteracion} ---")

        for t in tortugas:
            if t.finished:
                print(f"{t.nombre}: ya terminó ({t.distancia:.2f} m)")
                continue

            avance = t.mover()
            estado = f"{t.nombre}: +{avance:.2f} m -> {t.distancia:.2f} m"

            # Si cruzó la meta en este paso y aún no hay ganador, lo
            # anunciamos como ganador provisional.
            if t.finished and ganador is None:
                ganador = t
                print(estado + "  <-- ¡CRUZÓ LA META! (GANADOR provisional)")
            else:
                print(estado)

        if delay > 0:
            time.sleep(delay)

    # Todas han terminado
    if ganador is not None:
        print(f"\n¡La ganadora es {ganador.nombre} con {ganador.distancia:.2f} m!")
    else:
        print("\nNadie ganó (comportamiento inesperado).")

    print("Resultados finales:")
    # Ordenar por tiempo_finished si disponible, sino por distancia
    tortugas_sorted = sorted(
        tortugas,
        key=lambda x: (x.tiempo_finished if x.tiempo_finished is not None else float('inf')),
    )

    for i, t in enumerate(tortugas_sorted, start=1):
        finish_time_str = (
            f"{t.tiempo_finished:.3f}" if t.tiempo_finished is not None else "-"
        )
        print(f"{i}. {t.nombre}: {t.distancia:.2f} m  tiempo_finished={finish_time_str}")


def parse_args():
    p = argparse.ArgumentParser(description="Simulador de Carreras de Tortugas")
    p.add_argument("--n", type=int, default=5, help="Número de tortugas")
    p.add_argument("--seed", type=int, default=None, help="Semilla aleatoria")
    p.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Pequeña pausa entre iteraciones para ver la salida (segundos)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    run_race(n=args.n, seed=args.seed, delay=args.delay)


if __name__ == "__main__":
    main()
