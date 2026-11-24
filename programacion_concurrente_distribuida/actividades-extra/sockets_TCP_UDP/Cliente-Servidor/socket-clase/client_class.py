import socket

server = "127.0.0.1"
puerto = 12345

try:
    scliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    scliente.settimeout(100.0)
    scliente.connect((server,puerto))
    conectados = True

    print(f"Conectado a {server}:{puerto}")
except:
    print("Algo a fallado , no se puede conectar")

if conectados:
    print(f"conectado a {server}:{puerto}")
    activo = True

    while activo:

        try :
            mensaje = input(":")
            if mensaje.upper() != "SALIR":
                print(f"Enviando: {mensaje}")
                scliente.send(mensaje.encode())
                datos = scliente.recv(1024)
                print(f"Respuesta: {datos.decode()}")
            else:
                print(f"Salimos")
                activo = False
        except ConnectionResetError as E:
            try :
                print(f"Algo ha fallado  enviando{E}")
                sClient =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sClient.connect((server,puerto))
                sClient.send(mensaje.encode())
                datos = sClient.recv(1024)
                print(f"mensaje recibido => {datos.decode()}")

            except ConnectionResetError as CR:
                print("no se puede conectar")
                print(f"el mensaje {mensaje} no se a enviado")
                sClient =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sClient.connect((server,puerto))

        except   Exception as B:
            print(f"Algo ha fallado  {B}")
    sClient.close()