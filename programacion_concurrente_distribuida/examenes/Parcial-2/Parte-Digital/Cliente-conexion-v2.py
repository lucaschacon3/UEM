from  cliente_datos import enviar,recv


def enviar_numer(cliente_socket,numero,reader):
    enviar(cliente_socket,numero)
    resp = recv(reader)

    return resp


def enviar_fin_get_suma(cliente_socket,reader):
    enviar(cliente_socket,"FIN")
    resp = recv(reader)
    return resp
    