import socket
import threading

server = "127.0.0.1"
puerto = 12345

def atenderCliente(socketCli,socketServ):
    abierto = True
    while abierto:
        datos = socketCli.recv(1024)
        if not datos:
            print(f"{socketCli}: Se nos ha caido la conexion (o algo) y no hemos recibido datos")
            abierto = False
        else:
            print(f"{socketCli}: Los datos recibidos son: {datos.decode()}")
            socketCli.send("OK".encode())
        print(f"{sservidor}: Mensaje gestionado")
    print(f"El cliente ha cerrado su conexion")


sservidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sservidor.bind((server,puerto))
sservidor.listen(2)

print(f"Servidor escuchando en {server}:{puerto}")


listaHilos = []
x=True
while x:
    scliente, direccion=sservidor.accept()
    h = threading.Thread(target=atenderCliente,args=[scliente,sservidor])
    listaHilos.append(h)
    h.start()

for j in listaHilos:
    j.join()
    