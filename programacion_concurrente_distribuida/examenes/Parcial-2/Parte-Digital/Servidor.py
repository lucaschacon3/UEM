import socket                 # Librería para comunicación por red usando sockets (TCP/UDP)
import threading              # Librería para trabajar con hilos (un hilo por cliente)
import time                   # Para poder usar sleep() (esperas)
import random                 # Para generar números aleatorios (ej: tiempos aleatorios)

server_ip = "127.0.0.1"       # IP local (localhost). Solo acepta conexiones desde tu propio PC
server_port = 1234            # Puerto donde el servidor va a escuchar conexiones
maximo = 20                   # Límite: si la suma de un cliente llega o supera esto, se responde "MAX"

sumas = []                    # Lista global: guardará la suma de cada cliente en una posición fija
mutex = threading.Lock()      # Candado (lock) para evitar que varios hilos modifiquen 'sumas' a la vez


def manejamos_cliente(conn, index):
    # Función que atiende a un cliente (se ejecuta en un hilo)
    # conn  -> socket del cliente ya conectado
    # index -> posición en la lista 'sumas' que corresponde a este cliente

    total = 0                 # Suma acumulada SOLO para este cliente

    archivo = conn.makefile() # Convierte el socket en "archivo" para leer por líneas con readline()
    flag = True               # Control del bucle principal del cliente

    while flag:               # Mientras el cliente no termine, seguimos leyendo mensajes

        line = archivo.readline()  # Lee una línea completa (hasta '\n') enviada por el cliente

        if not line:              # Si no llega nada (cadena vacía), el cliente cerró conexión
            flag = False          # Terminamos el bucle
        else:
            mensaje = line.strip() # Quitamos espacios y '\n' para quedarnos con el texto limpio

            if mensaje == "FIN":  # Si el cliente envía FIN, significa que ya terminó de enviar números
                conn.send(f"SUMA{total}\n".encode())  # Enviamos la suma final (ojo: sale tipo "SUMA20")
                flag = False       # Cerramos el bucle (termina el cliente)
            else:
                n = int(mensaje)   # Convertimos el mensaje a número (asumes que siempre es válido)
                total += n         # Acumulamos la suma del cliente

                # SECCIÓN CRÍTICA: aquí varios hilos podrían tocar 'sumas' al mismo tiempo
                mutex.acquire()    # Bloqueamos el acceso a 'sumas' para evitar condiciones de carrera
                sumas[index] = total  # Guardamos la suma actual en la posición fija de este cliente
                mutex.release()    # Liberamos el lock para que otros hilos puedan usar 'sumas'

                if total >= maximo:     # Si la suma alcanzó o superó el máximo permitido
                    conn.send(b"MAX\n") # Respondemos "MAX" para que el cliente sepa que llegó al límite
                else:
                    time.sleep(random.randint(2, 5))  # Simulamos espera aleatoria (2 a 5 segundos)
                    conn.send(b"OK\n")                # Respondemos "OK" confirmando que sumó bien

    conn.close()              # Cerramos el socket de este cliente cuando termina su comunicación


def main():
    # Función principal del servidor: crea el socket, escucha y acepta clientes

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP (IPv4 + TCP)

    server_socket.bind(server_ip, server_port)  # Asigna el socket a la IP y puerto (reserva esa dirección
    server_socket.listen(2)                        # Pone al servidor en modo escucha (cola de hasta 2)

    print(f"Escuchando {server_ip},{server_port}") # Mensaje para confirmar que el servidor está listo

    while True:                                    # Bucle infinito: el servidor acepta clientes continuamente

        conn, cliente_address = server_socket.accept()  # Espera conexión de un cliente (bloquea hasta que llegue)
        print(f"Conecting... {cliente_address}")        # Muestra la IP/puerto del cliente conectado

        # Sección crítica: vamos a crear una posición en 'sumas' para este nuevo cliente
        mutex.acquire()              # Bloqueamos para que no choque con otros hilos
        index = len(sumas)           # El index del cliente será la siguiente posición libre en la lista
        sumas.append(0)              # Creamos su posición inicial con 0 (aún no sumó nada)
        mutex.release()              # Liberamos el lock

        # Creamos el hilo que atenderá a este cliente, pasando conn e index
        h1 = threading.Thread(target=manejamos_cliente, args=(conn, index))
        h1.start()                   # Arranca el hilo (el servidor vuelve al accept() para más clientes)


main()  # Llamamos a main() para arrancar el servidor
