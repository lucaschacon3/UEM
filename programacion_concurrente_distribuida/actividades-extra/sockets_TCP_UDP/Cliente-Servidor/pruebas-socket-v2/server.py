#IMPORTAMOS SOCKET
import socket

#DECLARAMOS NUESTRO SERVER_IP_PORT  
# IGUAL AL CLIENTE PARA LA COMUNICACION
server_ip ="127.0.0.1"
server_port = 12345

#CREAMOS EL SOCKET
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#CREAMOS UN BIND() PARA ESCUCHAR AL PUERTO DE ORIGEN CLIENT
server_socket.bind((server_ip,server_port))
#PRINT ESCUCHANDO MENSAJE DE PUERTO 
print(f"Escuchando ah {server_ip},{server_port}")
#creamos nuestra vairbale boolean en True
flag = True
#creamos nuestro bucle infinito
while flag:
    # creamos RECVFROM(1024) para recibir el mensaje de cliente
    data,client_address = server_socket.recvfrom(1024)
    #print de server del mensaje recibido del cliente con su PORT efimero de client
    print(f"Mensaje recibido de {client_address} : {data.decode()}")
#entra en esta condificion , si el cliente envia EXIT tambien el problema 
#Finaliza al igual que cliente, pq lo enviame mensaje bytes 
#data.decode() si es == "EXIT"
#ENTRA EN => FALSE
    if data.decode() == "exit":
        flag = False
# SI NO , ENTRA EN LA PRIMERA CONDICION
#PASA A ELSE: PARA QUE USUARIO RESPONSA LO Q ENVIO CLIENT
    else: 
        #ESCRIBE EL MENSAJE PARA CLIENT
        mensaje = input(f"Escribir mensaje a Client : ")
        #.SEDNTO() ENVIAMOS EL MENSAJE EN BYTE Q ESCRIBIO EL CLIENT
        #A LA MISMA DIRECCION DE CLIENT Q RECVFROM(1024)
        server_socket.sendto(mensaje.encode(),(client_address))
#CERRAMOS EL server_socket
server_socket.close()
#PRINT PQ ENTRA EN FINALIZAR EL SERVIDOR
print(f"Finalizando Servidor.....")
    

