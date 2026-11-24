from cliente_datos import connectar
# Importa la función connectar() que:
# - crea el socket TCP
# - conecta con el servidor
# - crea el reader (makefile) para leer por líneas

from cliente_negocio import enviar_numero, enviar_fin_get_suma
# Importa funciones de “negocio”:
# - enviar_numero(): envía un número y espera respuesta ("OK" o "MAX")
# - enviar_fin_get_suma(): envía "FIN" y espera la suma final ("SUMA...")

server_ip = "127.0.0.1"   # IP del servidor (localhost)
server_port = 1234        # Puerto del servidor (debe coincidir con el servidor)


def main():
    # Función principal del cliente: conecta y permite enviar números o FIN

    client_sock, reader = connectar(server_ip, server_port)
    # Conecta el cliente al servidor y obtiene:
    # - client_sock: socket para enviar
    # - reader: "archivo" para leer respuestas por líneas

    flag = True  # Variable para controlar el bucle del cliente

    while flag:  # Mientras no terminemos, seguimos preguntando al usuario
        user = input("NUMERO O FIN : ")
        # Pide al usuario que escriba un número o la palabra FIN

        if user == "FIN":  # Si el usuario escribe FIN, terminamos
            resp = enviar_fin_get_suma(client_sock, reader)
            # Enviamos FIN al servidor y esperamos la suma final

            print(f"Servidor : {resp}")  # Mostramos la respuesta final del servidor
            flag = False                 # Salimos del bucle
        else:
            numero = int(user)
            # Convertimos la entrada a entero (si el usuario escribe algo no numérico, aquí fallará)

            resp_server = enviar_numero(client_sock, reader, numero)
            # Enviamos el número al servidor y recibimos "OK" o "MAX"

            print(f"Servidor : {resp_server}")  # Mostramos la respuesta del servidor

            if resp_server == "MAX":
                # Si el servidor dice "MAX", significa que ya se alcanzó el máximo permitido
                # Entonces enviamos FIN automáticamente para pedir la suma final

                resp = enviar_fin_get_suma(client_sock, reader)
                # Enviamos FIN y esperamos la suma final

                print(f"Servidor : {resp}")  # Mostramos la suma final
                # OJO: aquí NO pones flag=False, así que el bucle podría seguir pidiendo input
                # (aunque el servidor puede cerrar, y luego el cliente podría fallar al leer/escribir)

    client_sock.close()
    # Cerramos el socket del cliente al finalizar


main()
# Ejecuta el cliente directamente
