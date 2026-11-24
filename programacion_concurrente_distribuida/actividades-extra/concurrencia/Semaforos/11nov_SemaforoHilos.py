import threading
import random
import time

'''
Tenemos un cine donde el de las taquillas está más quemao que la pipa' un indio, por lo que ha apagado el walkie
para que nadie le moleste mientras vende entradas.

Por otro lado, a los 30 segundos de empezar a venderse entradas, se declara un incendio en la sala del cine
y tienen que venir los bomberos a sacar a la gente por dos salidas de emergencia.

Cada salida de emergencia puede sacar a dos personas a la vez.

Hay gente ya en la sala? Sí. Puede haber entre 20 y 30 personas aleatoriamente.

Cuantas entradas se venden a la vez? Se pueden vender de 1 a 5 entradas en cada venta.

Cuanto tardamos en vender las entradas? 3 segundos por entrada.

Aforo de la sala: No revendemos entradas al quemar gente, así que el aforo tiene que ser fijo (max 100 personas).

Puede salir una persona individual.

Velocidad de salida por la puerta aleatoria (entre 10 y 15 segundos)
'''

mutex = threading.Lock()

# Aforo máximo
AFORO_MAXIMO = 100

# Personas iniciales en la sala
personas_sala = random.randint(20, 30)

# Semáforo para SALIDAS (cada salida puede evacuar 2 personas)
salida1 = threading.Semaphore(2)
salida2 = threading.Semaphore(2)

# Variable de control para detener ventas
incendio = False


def vender_entradas():
    global personas_sala
    global incendio

    while not incendio:
        # Venta entre 1 y 5 entradas
        entradas = random.randint(1, 5)

        # Comprobar aforo antes de vender
        if personas_sala + entradas <= AFORO_MAXIMO:
            # Tardar 3 segundos por entrada
            tiempo_venta = entradas * 3
            print(f"[TAQUILLA] Vendiendo {entradas} entradas… ({tiempo_venta}s)")

            time.sleep(tiempo_venta)

            # Actualizar personas dentro de sala
            ok = mutex.acquire(timeout=2)
            if ok:
                personas_sala = personas_sala + entradas
                print(f"[TAQUILLA] Entradas vendidas. En sala ahora hay {personas_sala} personas.")
                mutex.release()

        else:
            print("[TAQUILLA] Aforo lleno, no puedo vender más entradas.")
            time.sleep(2)


def evacuar_personas(nombre_salida, semaforo_salida):
    global personas_sala
    global incendio

    while incendio:
        ok = semaforo_salida.acquire(timeout=1)

        if ok:
            ok2 = mutex.acquire(timeout=1)
            if ok2:
                if personas_sala > 0:
                    personas_sala = personas_sala - 1
                    persona_actual = personas_sala
                    mutex.release()

                    tiempo_salida = random.randint(10, 15)
                    print(f"[{nombre_salida}] Saliendo persona… tarda {tiempo_salida}s | Quedan: {persona_actual}")
                    time.sleep(tiempo_salida)

                else:
                    mutex.release()
                    semaforo_salida.release()
                    time.sleep(1)
            else:
                semaforo_salida.release()
                time.sleep(1)
        else:
            time.sleep(1)


def activar_incendio():
    global incendio
    time.sleep(30)
    incendio = True
    print("\n¡INCENDIO EN LA SALA! Comienza evacuación 🔥🔥🔥\n")


def main():
    global personas_sala
    print(f"Personas iniciales en la sala: {personas_sala}")

    # Hilo taquilla
    h_taquilla = threading.Thread(target=vender_entradas)

    # Hilo incendio
    h_incendio = threading.Thread(target=activar_incendio)

    # Hilos de evacuación
    h_salida_1 = threading.Thread(target=evacuar_personas, args=("Salida 1", salida1))
    h_salida_2 = threading.Thread(target=evacuar_personas, args=("Salida 2", salida2))

    # Iniciar hilos
    h_taquilla.start()
    h_incendio.start()

    # Esperar al incendio
    h_incendio.join()

    # Iniciar evacuaciones
    h_salida_1.start()
    h_salida_2.start()

    # Unir hilos
    h_salida_1.join()
    h_salida_2.join()

    print("\nEVACUACIÓN COMPLETAAAAA\n")


if __name__ == "__main__":
    main()
