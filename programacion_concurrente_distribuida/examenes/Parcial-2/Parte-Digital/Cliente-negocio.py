from cliente_datos import enviar_linea, recv_linea
# Importamos funciones auxiliares:
# - enviar_linea(): envía texto/números al servidor terminados en '\n'
# - recv_linea(): lee una línea completa desde el servidor


def enviar_numero(client_sock, reader, numero):
    # Envía un número al servidor y espera una respuesta ("OK" o "MAX")
    # client_sock -> socket del cliente (para enviar)
    # reader      -> archivo de lectura asociado al socket (para recibir)
    # numero      -> número que queremos enviar al servidor

    enviar_linea(client_sock, numero)  # Envía el número al servidor como una línea (ej: "5\n")

    resp = recv_linea(reader)          # Espera y lee la respuesta del servidor ("OK" o "MAX")

    return resp                        # Devuelve la respuesta al programa principal


def enviar_fin_get_suma(client_sock, reader):
    # Envía el mensaje "FIN" al servidor y espera la suma final
    # client_sock -> socket del cliente
    # reader      -> archivo de lectura

    enviar_linea(client_sock, "FIN")   # Envía "FIN\n" para indicar que ya no habrá más números

    resp = recv_linea(reader)          # Lee la respuesta final del servidor (ej: "SUMA20")

    return resp                        # Devuelve la suma recibida
