import socket

def connectar(ip,port):

    cliente_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cliente_socket.connect((ip,port))

    archivo = cliente_socket.makefile("r")

    return cliente_socket, archivo


def enviar(cliente_socket,text):
    cliente_socket.send((str(text) + "\n").encode())

def recv (reader):

    linea = reader.readline()

    return linea


