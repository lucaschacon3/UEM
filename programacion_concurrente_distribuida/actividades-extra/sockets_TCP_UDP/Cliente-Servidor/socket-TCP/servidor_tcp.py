import socket

server = "127.0.0.1"
puerto = 12345

sservidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sservidor.bind((server,puerto))
sservidor.listen(2)

print(f"Servidor escuchando en {server}:{puerto}")



while True:
    scliente, direccion=sservidor.accept()
    datos = scliente.recv(1024)
    if not datos:
        print(f"{scliente}: Se nos ha caido la conexion (o algo) y no hemos recibido datos")
    else:
        print(f"{scliente}: Los datos recibidos son: {datos.decode()}")
        scliente.send("OK".encode())
    print(f"{sservidor}: Mensaje gestionado")
    