#IMPORTAMOS SOCKET
import socket 
#INICIALIZAMOS SERVIDOR IP Y PUERTO
server_ip ="127.0.0.1"
server_port = 12345
#INICIALIZAMOS EL SOCKET
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#CREAMOS NUESTA BOOLEAN
flag = True
#CREAMOS NUESTRO BUCLE INFINITO
while flag:
    #AÑADIMOS UN INPUT PARA ENVIAR EL MENSAJE 
    mensaje = input("Escribir mensaje UDP :")
#CONDICIONAMOS CON IF SI NUESTRO MENSAJE ES
#"EXIT" NUESTO BUCLE SE DETIENE Y ENVIE 
#MENSAJE AL SERVIDOR PARA DETENERLO TAMBIEN 
    if mensaje == "exit":
        #ENVIAMOS IGUAL LA MENSAJE "EXIT"
        client_socket.sendto(mensaje.encode(),(server_ip,server_port))
        #CUANDO ES EXIT ES FALSE
        flag = False
    # AQUI SI NO CUMPLE NUESTRA CONDICION QUE ENTRE AQUI 
    # Y SE ENVIE EL MENSAJE DE LO Q NO ENTRO EN EL IF 
    else:
        #ENVIAMOS MENSAJE AL SERVIDOR EN BYTES Y AL PUERTO DESTINO
        client_socket.sendto(mensaje.encode(),(server_ip,server_port))
        #AQUI TAMBIEN RECIBIMOS EN BYTES EL MENSAJE DE NUESTRO SERVIDOR
        data,server_address = client_socket.recvfrom(1024)
        #PRINTEAMOS EL MENAJE RECIBIDO DEL SERVIDOR, ORIGEN Y EN BYTES
        print(f"Mensaje recibido de {server_address} : {data.decode()}")
#CERRAMOS EL SOCKET SI CUMPLE LA PRIMERA CONDICION EXIT 
client_socket.close()
#SE IMPRIME ESTA LINEA SI , NUESTRO CLIENT ESCRIBE EXIT 
print("Finalizando client, Gracias ....")