# SERVIDOR
#IMPORTAMOS MODULO SOCKET PARA COMUNICACION EN RED
import socket
# IP Y PUERTO DEL SERVIDOR PARA ESCUCHAR MENSAJES
#DEBE COINCIDIR CON LOS DEL CLIENTE
server_ip = "127.0.0.1"
server_port = 12345
#CREAMOS SOCKETS DEL SERVIDOR 
#socket.AF_INET => USA IPV4
#socket.SOCK_DGRAM => PARA UDP
# => CLIENTE Y SERVIDOR USAN EL MISMO SOCKETS
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ======> bind() => ESTE PROGRAMA ESCUCHA EN ESTA IP Y PUERTO
server_socket.bind((server_ip, server_port))
#MENSAJE INFORMATIVO DE Q EL SERVIDOR ESCUCHA A CLIENTE
print(f"Servidor escuchando en {server_ip}:{server_port}")
# BUCLE INFINITO para que el servidor siempre este escuchando mensaje

while True:
    #recibe mensaje , datos de cliente
    #=> recvfrom(1024) ==>  espera un mensaje de hasta 1024 bytes
    # Devuelve data y client_address IP y puerto del cliente
    data, client_address = server_socket.recvfrom(1024)
    # MUESTA EL MENSAJE RECIBIDO 
    #client_address => DIRECCION DEL CLIENTE / quien envio el mensaje 
    #data.decode() ==> CONVIERTE BYTES A STRING
    print(f"Mensaje recibido desde => {client_address}: {data.decode()}")
# CERRAR EL SOCKET DEL SERVIDOR (NUNCA SE LLEGA AQUI EN ESTE EJEMPLO)
server_socket.close()