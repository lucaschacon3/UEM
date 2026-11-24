import socket

server = "127.0.0.1"
puerto = 12345

scliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

scliente.settimeout(100.0)
scliente.connect((server,puerto))


print(f"Conectado a {server}:{puerto}")

while True:
    mensaje = input(":")
    print(f"Enviando: {mensaje}")
    scliente.send(mensaje.encode())
    datos = scliente.recv(1024)
    print(f"Respuesta: {datos.decode()}")