import socket


#servidor.py
#D:\Usuario marbe\Desktop\UEM\3er CURSO\PROGRAMACIÓN CONCURRENTE Y DISTRIBUIDA\PCD> python Servidor_EXAM2_PARTE_ESCRITA.py

# ===========================
# CONFIGURACIÓN INICIAL
# ===========================
HOST = 'localhost'       # Dirección del servidor (localhost = esta máquina)
PUERTO = 12345           # Puerto en el que el servidor estará escuchando conexiones
contador = 0             # Variable que irá acumulando la suma de los números recibidos


# ===========================
# CREACIÓN DEL SERVIDOR
# ===========================
# Creamos el socket: AF_INET = IPv4, SOCK_STREAM = protocolo TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignamos dirección y puerto al socket
servidor.bind((HOST, PUERTO))

# El servidor empieza a escuchar conexiones entrantes
servidor.listen()

print("Servidor escuchando en el puerto", PUERTO)

# Esperamos a que un cliente se conecte (bloqueante)
conn, addr = servidor.accept()
print("Conectado con", addr)  # Mostramos la dirección del cliente conectado

# ===========================
# BUCLE PRINCIPAL DEL SERVIDOR
# ===========================
conexion_activa = True  # Bandera booleana para controlar el bucle (no usamos break)

while conexion_activa:
    # Recibimos datos desde el cliente (hasta 1024 bytes) y los decodificamos (de bytes a texto)
    datos = conn.recv(1024).decode()
    
    if not datos:
        # Si no recibimos nada, cerramos la conexión
        conexion_activa = False
    elif datos == "FIN":
        # Si el cliente envía "FIN", se termina la comunicación
        print("Se recibió FIN. Cerrando servidor.")
        conexion_activa = False
    else:
        try:
            # Convertimos el mensaje recibido en entero y lo sumamos al contador
            numero = int(datos)
            contador += numero

            # Mostramos el número recibido y la suma acumulada
            print("Número recibido:", numero, "- Total acumulado:", contador)

            # Enviamos confirmación al cliente en formato de bytes
            conn.sendall(b"OK")  # b"" es para enviar texto como bytes
        except ValueError:
            # Si lo recibido no es un número válido, respondemos con "ERROR"
            print("Dato inválido:", datos)
            conn.sendall(b"ERROR")  # b"" convierte la cadena a bytes automáticamente

# ===========================
# CIERRE DE CONEXIÓN
# ===========================
conn.close()        # Cerramos la conexión con el cliente
servidor.close()    # Cerramos el socket del servidor
