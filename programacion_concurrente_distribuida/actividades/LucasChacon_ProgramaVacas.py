"""
Ejecución:  python3 LucasChacon_ProgramaVacas.py   (Python 3, solo biblioteca estándar)

Cómo se coordinan los hilos (mecanismos del Tema 2):

- mutex_campo (threading.Lock): protege TODO el estado compartido del juego
  (terreno, posición de la vaca, posiciones de los tractores, contadores y la
  marca de fin). Tanto las lecturas como las escrituras se hacen con el mutex
  cogido; nadie duerme ni pinta con el mutex puesto.

- plazas_tractor (threading.Semaphore(2)): controla cuántos tractores hay
  dentro del campo. Nunca puede haber más de 2: se hace acquire(timeout=3)
  antes de entrar y exactamente un release() al salir (en un finally).

- cola_cacas (queue.Queue): transporta cada caca (fila, columna, instante)
  desde la vaca (productor, put) hasta el hilo de la hierba (consumidor,
  get(timeout=...)). No hay otra lista compartida para las cacas.

- Por qué no hay deadlock (regla del orden fijo): todo hilo que necesite dos
  mecanismos los adquiere siempre en el mismo orden: PRIMERO el semáforo
  plazas_tractor, DESPUÉS el mutex_campo. Nunca se espera a plazas_tractor
  teniendo cogido mutex_campo, por lo que no puede formarse el ciclo
  «A espera el semáforo con el mutex / B espera el mutex con el semáforo».
  La cola se usa sin mutex (get con timeout) y put sobre cola ilimitada no
  bloquea, así que tampoco genera esperas cruzadas.
"""

import queue
import random
import threading
import time

DISTANCIA_HIERBA = 10          # segundos que tarda en rebrotar la hierba
LIMITE_TIEMPO = 180            # 3 minutos
MOVIMIENTOS_VACA_CACA = 5      # cada N movimientos la vaca deja una caca
MOVIMIENTOS_GRANJERO = 10

DESPLAZAMIENTOS = {1: (-1, 0), 2: (0, 1), 3: (1, 0), 4: (0, -1)}  # N, E, S, O

estado = {
    "terreno": [],           # lista de listas: '"', '.' u 'O'
    "alto": 0,
    "ancho": 0,
    "vaca": (0, 0),          # (fila, columna)
    "tractores": {},         # nombre del granjero -> (fila, columna)
    "recogidas": 0,
    "movimientos_vaca": 0,
    "fin": False,
    "motivo": "",
}

# Orden fijo de adquisición en todo el programa: plazas_tractor antes que
# mutex_campo (evita el deadlock por adquisición cruzada semáforo/mutex).
mutex_campo = threading.Lock()
plazas_tractor = threading.Semaphore(2)
cola_cacas = queue.Queue()


def juego_terminado():
    with mutex_campo:
        return estado["fin"]


def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print(f"Dato no válido: introduce un entero entre {minimo} y {maximo}.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"Dato no válido: debe estar entre {minimo} y {maximo}.")


def pedir_posicion_vaca(alto, ancho):
    while True:
        fila = pedir_entero("Fila inicial de la vaca (0 a {}): ".format(alto - 1), 0, alto - 1)
        col = pedir_entero("Columna inicial de la vaca (0 a {}): ".format(ancho - 1), 0, ancho - 1)
        if (fila, col) == (0, 0):
            print("La vaca no puede empezar en (0, 0): es la entrada de los tractores.")
            continue
        return fila, col


def preparar_estado():
    ancho = pedir_entero("Ancho del terreno (4 a 8): ", 4, 8)
    alto = pedir_entero("Alto del terreno (4 a 8): ", 4, 8)
    fila, col = pedir_posicion_vaca(alto, ancho)
    estado["alto"] = alto
    estado["ancho"] = ancho
    estado["terreno"] = [['"' for _ in range(ancho)] for _ in range(alto)]
    estado["vaca"] = (fila, col)
    estado["tractores"] = {}
    estado["recogidas"] = 0
    estado["movimientos_vaca"] = 0
    estado["fin"] = False
    estado["motivo"] = ""


def dentro_del_terreno(fila, col):
    return 0 <= fila < estado["alto"] and 0 <= col < estado["ancho"]


def hay_alguien_en(fila, col, excluir=None):
    if estado["vaca"] == (fila, col):
        return True
    for nombre, pos in estado["tractores"].items():
        if nombre != excluir and pos == (fila, col):
            return True
    return False


# ---------------------------------------------------------------------------
# Vaca
# ---------------------------------------------------------------------------

def mover_vaca():
    """Comprueba y mueve en la MISMA sección crítica (sin soltar el mutex)."""
    with mutex_campo:
        fila, col = estado["vaca"]
        for _ in range(10):
            df, dc = DESPLAZAMIENTOS[random.randint(1, 4)]
            nf, nc = fila + df, col + dc
            # Fuera del terreno o casilla ocupada por un tractor: otro intento
            if not dentro_del_terreno(nf, nc):
                continue
            if (nf, nc) in estado["tractores"].values():
                continue
            if estado["terreno"][nf][nc] == '"':
                estado["terreno"][nf][nc] = "."  # se come la hierba
            estado["vaca"] = (nf, nc)
            estado["movimientos_vaca"] += 1
            if (estado["movimientos_vaca"] % MOVIMIENTOS_VACA_CACA == 0
                    and estado["terreno"][nf][nc] != "O"):
                estado["terreno"][nf][nc] = "O"
                # La caca viaja solo por la cola hacia el hilo de la hierba
                cola_cacas.put((nf, nc, time.time()))
            return True
    # Tras 10 intentos no hay casilla libre: el llamador espera y reintenta
    return False


def hilo_vaca():
    while not juego_terminado():
        mover_vaca()
        # Espera entre movimientos FUERA del mutex
        time.sleep(random.randint(2, 5) / 10)


# ---------------------------------------------------------------------------
# Hierba (consumidor de la cola de cacas)
# ---------------------------------------------------------------------------

def hilo_hierba():
    while not juego_terminado():
        try:
            # timeout para no quedarse bloqueada al terminar la partida
            fila, col, instante = cola_cacas.get(timeout=0.5)
        except queue.Empty:
            continue  # no hay cacas: volver a comprobar el fin
        espera = instante + DISTANCIA_HIERBA - time.time()
        if espera > 0:
            time.sleep(espera)  # dormir FUERA del mutex
        with mutex_campo:
            if estado["fin"]:
                break
            # Solo rebrota si la caca sigue allí (un tractor pudo recogerla)
            if estado["terreno"][fila][col] == "O":
                estado["terreno"][fila][col] = '"'


# ---------------------------------------------------------------------------
# Granjeros (3 hilos con tractor)
# ---------------------------------------------------------------------------

def entrar_en_campo(nombre):
    """Coloca el tractor en (0, 0) si está libre: comprobar y ocupar en el
    mismo with. Si está ocupada, espera fuera del mutex y reintenta."""
    while not juego_terminado():
        with mutex_campo:
            if not hay_alguien_en(0, 0):
                estado["tractores"][nombre] = (0, 0)
                return True
        time.sleep(0.1)  # fuera del mutex: ceder el turno sin ocupación activa
    return False


def mover_tractor(nombre):
    """Sortea una dirección y avanza hasta 2 casillas, todo dentro de un
    solo with: la comprobación y el avance no se separan."""
    with mutex_campo:
        if nombre not in estado["tractores"]:
            return
        fila, col = estado["tractores"][nombre]
        df, dc = DESPLAZAMIENTOS[random.randint(1, 4)]
        for _ in range(2):
            nf, nc = fila + df, col + dc
            if not dentro_del_terreno(nf, nc):
                break  # borde: se para antes
            if hay_alguien_en(nf, nc, excluir=nombre):
                break  # casilla ocupada: se para antes
            fila, col = nf, nc
            if estado["terreno"][fila][col] == "O":
                # Se detiene en la caca y la recoge
                estado["terreno"][fila][col] = "."
                estado["recogidas"] += 1
                break
            # Si pasa por hierba, esta se queda donde estaba
        estado["tractores"][nombre] = (fila, col)


def salir_del_campo(nombre):
    with mutex_campo:
        estado["tractores"].pop(nombre, None)


def trabajar_en_el_campo(nombre):
    if not entrar_en_campo(nombre):
        return
    try:
        for _ in range(MOVIMIENTOS_GRANJERO):
            if juego_terminado():
                break
            mover_tractor(nombre)
            # Entre movimiento y movimiento: dormir FUERA del mutex
            time.sleep(random.randint(5, 10) / 10)
    finally:
        # Sale siempre del terreno y deja libre su plaza en el semáforo
        # (el release del semáforo lo hace el hilo en su propio finally)
        salir_del_campo(nombre)


def hilo_granjero(nombre):
    while not juego_terminado():
        # Orden fijo: PRIMERO el semáforo (sin el mutex), DESPUÉS el mutex
        # dentro de trabajar_en_el_campo. Así no se puede dar un deadlock
        # por esperar el semáforo con el mutex cogido.
        if plazas_tractor.acquire(timeout=3):
            try:
                trabajar_en_el_campo(nombre)
            finally:
                plazas_tractor.release()  # exactamente 1 release por acquire
        # Descanso entre 2 y 4 segundos (también si no hubo plaza)
        time.sleep(random.randint(2, 4))


# ---------------------------------------------------------------------------
# Pintor (único que escribe en pantalla durante la partida)
# ---------------------------------------------------------------------------

def dibujar(copia, vaca, tractores):
    filas = [list(f) for f in copia]
    for tr in tractores:
        if dentro_del_terreno(*tr):
            filas[tr[0]][tr[1]] = "T"
    if dentro_del_terreno(*vaca):
        filas[vaca[0]][vaca[1]] = "V"
    print("\033[2J\033[H", end="")  # limpiar pantalla
    print("Vacas y cacas  (V vaca, T tractor, \" hierba, O caca, . vacía)")
    for fila in filas:
        print(" ".join(fila))


def resumen_linea(hierba, cacas, recogidas, tractores):
    print(f" hierba: {hierba} | cacas en el campo: {cacas} | "
          f"cacas recogidas: {recogidas} | tractores dentro: {tractores}")


def hilo_pintor():
    inicio = time.time()
    while True:
        # Copiar dentro, soltar el mutex y pintar fuera (la consola es lenta)
        with mutex_campo:
            copia = [fila[:] for fila in estado["terreno"]]  # copia profunda por filas
            vaca = estado["vaca"]
            tractores = list(estado["tractores"].values())
            hierba = sum(fila.count('"') for fila in estado["terreno"])
            cacas = sum(fila.count("O") for fila in estado["terreno"])
            recogidas = estado["recogidas"]
            n_tractores = len(tractores)
            if not estado["fin"]:
                if hierba == 0:
                    estado["fin"] = True
                    estado["motivo"] = "no queda ninguna casilla con hierba"
                elif time.time() - inicio >= LIMITE_TIEMPO:
                    estado["fin"] = True
                    estado["motivo"] = f"límite de {LIMITE_TIEMPO // 60} minutos"
            fin = estado["fin"]
        # --- fuera del mutex ---
        dibujar(copia, vaca, tractores)
        resumen_linea(hierba, cacas, recogidas, n_tractores)
        if fin:
            break
        time.sleep(1)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    preparar_estado()

    hilos = [
        threading.Thread(target=hilo_vaca, name="Vaca"),
        threading.Thread(target=hilo_hierba, name="Hierba"),
        threading.Thread(target=hilo_pintor, name="Pintor"),
        threading.Thread(target=hilo_granjero, args=("Granjero-0",), name="Granjero-0"),
        threading.Thread(target=hilo_granjero, args=("Granjero-1",), name="Granjero-1"),
        threading.Thread(target=hilo_granjero, args=("Granjero-2",), name="Granjero-2"),
    ]

    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()  # todos terminan por sí mismos: nada de daemon ni exit

    with mutex_campo:
        hierba = sum(fila.count('"') for fila in estado["terreno"])
        cacas = sum(fila.count("O") for fila in estado["terreno"])
        recogidas = estado["recogidas"]
        n_tractores = len(estado["tractores"])
        motivo = estado["motivo"]

    print("--------------------------------")
    print(f"Partida terminada ({motivo}).")
    print(f"Terreno de {estado['alto']} x {estado['ancho']} filas x columnas.")
    print(f"Vaca final en {estado['vaca']}.")
    resumen_linea(hierba, cacas, recogidas, n_tractores)


if __name__ == "__main__":
    main()
