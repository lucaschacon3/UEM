import socket       # Importamos socket para la comunicación cliente-servidor
import random       # Para generar números aleatorios
import time         # Para pausas entre envíos

#cliente.py
#D:\Usuario marbe\Desktop\UEM\3er CURSO\PROGRAMACIÓN CONCURRENTE Y DISTRIBUIDA\PCD> python Cliente_EXAM2_PARTE_ESCRITA.py

# ===========================
# CONFIGURACIÓN DEL CLIENTE
# ===========================
HOST = 'localhost'        # Dirección del servidor al que se conectará (localhost = esta máquina)
PUERTO = 12345            # Puerto donde el servidor está escuchando
CANTIDAD_NUMEROS = 10     # Cantidad de números aleatorios que se enviarán

# ===========================
# CREACIÓN DEL SOCKET CLIENTE
# ===========================
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creamos socket TCP IPv4
cliente.connect((HOST, PUERTO))                              # Nos conectamos al servidor en HOST y PUERTO

# ===========================
# ENVÍO DE NÚMEROS ALEATORIOS
# ===========================
for _ in range(CANTIDAD_NUMEROS):
    numero = random.randint(1, 10)                  # Generamos un número aleatorio entre 1 y 10
    
    # Enviamos el número convertido a cadena, luego a bytes con .encode()
    cliente.sendall(str(numero).encode())           
    
    # Esperamos la respuesta del servidor (como bytes) y la decodificamos a texto
    respuesta = cliente.recv(1024).decode()
    
    # Mostramos en consola lo que enviamos y la respuesta recibida
    print("Enviado:", numero, "- Respuesta del servidor:", respuesta)
    
    time.sleep(0.5)  # Pausa para simular tiempo entre envíos

# ===========================
# FINALIZACIÓN DE LA CONEXIÓN
# ===========================
cliente.sendall(b"FIN")   # Enviamos la palabra FIN para indicar que terminamos
cliente.close()           # Cerramos la conexión con el servidor

print("Cliente ha terminado.")  # Mensaje final para indicar que terminó el cliente
