#importamos el socket
import socket
#direccion y puerto del TCP
server_ip = "127.0.0.1"
server_port = 12345
#CREAMOS EL SOCKET 
#socket.AF_INET IPV4
#PROTOCOLO DE TRANSPORTE TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#EL PROTOCOLO TCP SE CONECTA AL SERVIDOR 
#SO ASIGNA PUERTO EFIMERO A CLIENT
client_socket.connect((server_ip, server_port))
#PRINT
print("Conectado al servidor TCP")
#VARIABLE CONTROLA EL BUCLE
flag = True
#BUCLE

while flag:
#INPUT 
    mensaje = input("Enviar mensaje TCP : ")
#ENVIA EL MENSAJE AL SERVIDOR POR LA CONEXION TCP
    client_socket.send(mensaje.encode())
#SI EL USUARIO ESCRIBE EXIT
#NO SE ESPERA RESPUES
#SALE DEL PROGRAMA
    if mensaje == "exit":
        flag = False
    #SI NO ESTA FUERA DEL  PROGRAMA
    #ENTRA ELSE
    else:
        #SI NO ES EXIT ENTRA AQUI
        data = client_socket.recv(1024)
    #PRINTER DE MENSAJE RECIBIDO DEL SERVIDOR EN BYTES
        print(f"Mensaje recibido del servidor : {data.decode()}")
#CERRAMOS EL SOCKET ...
client_socket.close()
print("Cliente TCP finalizado...")
