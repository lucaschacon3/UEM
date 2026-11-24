#IMPORTAMOS EL SOCKET 
import socket
#CREAMOS LAS VARIABLES DEL PUERTO FIJOS DEL SERVIDOR
server_ip = "127.0.0.1"
server_port = 12345
#CREAMOS EL SOCKET => TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ESCUCHAMOS EL PUERTO FIJO , COMO UDP
server_socket.bind((server_ip, server_port))
#EL SERVIDOR QUEDA ESCUCHANDO ACEPTA CONEXCION TCP
# 1 CLIENTE EN COLA 
server_socket.listen(1)
#PRINTER MENSAJE INFORMATIVO
print(f"Servidor TCP escuchando en {server_ip}:{server_port}")
#accept() ESPERA QUE CLIENTE SE CONECTE
#conn NUEVO SOCKET PARA COMUNICARTE CON ESE CLIENTE
conn, client_address = server_socket.accept()
#MUESTA IP PUERTO EFIMERO DEL CLIENTE
print(f"Cliente conectado desde {client_address}")
#NUESTRO BOLEANO , PARA CONTROLAR EL BUCLE
flag = True
#BUCLE INFINITO
while flag:
    #RECIBE DATO DEL CLIENTE TCP
    data = conn.recv(1024)
    mensaje_cliente = data.decode()
    #LO DECODIFICA EL MENSAJE RECIBIDO DE CLIENT
    print(f"Mensaje recibido : {mensaje_cliente}")
#SI, LA PALABRA ES EXIT, SALIMOS DEL BUCLE INFINITO Y FINALIZAMOS SERVER
    if mensaje_cliente == "exit":
        flag = False
    #SI, NO ES EXIT... ENTRAMOS EN ELSE...
    else:
        respuesta = input("Enviar mensaje al cliente TCP : ")
        #USANDO SOCKET QUE ESTA CONECTADO
        conn.send(respuesta.encode())
#cerramos conexion con el cliente 
conn.close()
#cerramos socket que escucha....
server_socket.close()
print("Servidor TCP finalizado...")
