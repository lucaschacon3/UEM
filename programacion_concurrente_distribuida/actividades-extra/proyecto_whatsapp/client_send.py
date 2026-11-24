import socket  # Librería de sockets (TCP/UDP). Aquí usas TCP (SOCK_STREAM)

from protocol import socket_send_line, socket_recv_line, parse_record, timestamp_now
# socket_send_line(): envía una línea por el socket según tu framing (probablemente añade \n)
# socket_recv_line(): recibe una línea usando un buffer acumulado (devuelve ok, linea, buf_actualizado)
# parse_record(): parsea registros tipo "origen;destino;ts;estado;tsst;msg"
# timestamp_now(): genera un timestamp en el formato del sistema

from storage import read_lines, write_lines, merge_record
# read_lines(): lee líneas de un archivo y devuelve lista
# write_lines(): escribe lista de líneas en un archivo (sobreescribe)
# merge_record(): añade un registro a un archivo conversación (normalmente evitando duplicados o manteniendo orden)


def connect_port(ip, port, timeout, user, pwd):  # Conecta a un puerto TCP del servidor y hace login básico
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP IPv4
    s.settimeout(timeout)                                  # Configura timeout para operaciones de socket

    try:
        s.connect((ip, port))                               # Intenta conectarse a (ip, port)
    except Exception:                                       # Si falla la conexión
        try:
            s.close()                                       # Intenta cerrar socket
        except Exception:
            x = 0                                           # Código “dummy” (no hace falta en Python)
            x = x + 1
        return False, None, b""                             # Devuelve: no ok, sin socket, buffer vacío

    buf = b""                                               # Buffer para el protocolo de recepción por líneas
    socket_send_line(s, "LOGIN:" + user + ":" + pwd)        # Envía línea de login al servidor
    ok, resp, buf = socket_recv_line(s, buf)                # Espera respuesta (OK/KO/lo que sea)

    if ok and resp == "OK":                                 # Si recibió algo y fue OK
        return True, s, buf                                 # Conexión y login correctos

    try:
        s.close()                                           # Si login falla, cierra socket
    except Exception:
        x = 0                                               # Dummy otra vez
        x = x + 1
    return False, None, b""                                 # Devuelve fallo


def send_exists(sock, buf, target_user):  # Pregunta al servidor si existe un usuario
    # Mini-protocolo interno:
    # EXISTS:User  -> OK si existe, KO => no existe
    line = "EXISTS:" + target_user                          # Construye la petición EXISTS
    ok = socket_send_line(sock, line)                       # Envía la petición al servidor
    if not ok:                                              # Si no se pudo enviar
        return False, buf, False                            # (fallo comunicación, buffer, exists False)

    ok2, resp, buf = socket_recv_line(sock, buf)            # Lee respuesta del servidor
    if not ok2:                                             # Si no se pudo recibir correctamente
        return False, buf, False                            # Fallo comunicación

    if resp == "OK":                                        # Si servidor dice OK
        return True, buf, True                              # Existe
    return True, buf, False                                 # Si no es OK, asumimos que no existe


def send_record(send_sock, send_buf, line):  # Envía 1 “registro” (mensaje) y espera OK/KO del servidor
    # Enviar 1 línea; esperar OK/KO
    ok = socket_send_line(send_sock, line)                  # Envía el registro al servidor
    if not ok:                                              # Si falló el envío
        return False, send_buf, "", ""                      # Comunicación fallida

    ok2, ack, send_buf = socket_recv_line(send_sock, send_buf)  # Recibe ACK del servidor y actualiza buffer
    if not ok2:                                             # Si no pudo recibir ACK
        return False, send_buf, "", ""                      # Comunicación fallida

    if ack == "OK":                                         # Caso normal: servidor aceptó el registro
        return True, send_buf, "OK", ""                     # Devuelve estado OK sin error

    if ack == "KO":                                         # Caso error: servidor rechazó el registro
        # Según tu diseño: si KO, el server manda una línea extra con ERROR
        ok3, err_line, send_buf = socket_recv_line(send_sock, send_buf)  # Lee línea extra con detalle del error
        if ok3:                                             # Si pudo leer el error
            socket_send_line(send_sock, "OK")               # Confirma al servidor que recibió la línea de error
            return True, send_buf, "KO", err_line           # Devuelve KO y el registro de error
        return True, send_buf, "KO", ""                     # Si no pudo leer detalle, KO sin detalle

    # Si llega algo distinto a OK/KO
    return True, send_buf, ack, ""                          # Devuelve “ack” tal cual (raro, pero lo expones)


def send_fin(send_sock, send_buf):          # Envía FIN al servidor para cerrar “bien” la sesión/canal
    socket_send_line(send_sock, "FIN")      # Envía FIN
    ok, resp, send_buf = socket_recv_line(send_sock, send_buf)  # Espera respuesta (aunque no la validas)
    return send_buf                         # Devuelve buffer actualizado (por consistencia con el resto)


def _convert_enviado_to_recibido(line):     # Convierte una línea local ENVIADO a RECIBIDO para mandarla al server
    okr, o, d, ts, st, tsst, msg = parse_record(line)  # Intenta parsear el registro local
    if not okr:                                         # Si no se pudo parsear
        return False, ""                                # Indica fallo

    if st != "ENVIADO":                                 # Si no está en estado ENVIADO
        return True, line.strip()                       # No hace falta convertir, la devuelve “limpia”

    # Cambiamos estado para enviar al server como mensaje real (no local)
    # TiempoEstado lo ponemos "000..." porque el server lo rellenará si quiere,
    # o lo ponemos ahora mismo. Para simplificar: ahora mismo.
    new_line = o + ";" + d + ";" + ts + ";RECIBIDO;" + timestamp_now() + ";" + msg
    # Construye el nuevo registro con estado RECIBIDO y tsst = timestamp_now()
    return True, new_line                               # Devuelve la línea convertida


def flush_tmp_for_peer(send_sock, send_buf, tmp_path, conv_path):  # Reenvía al server los mensajes guardados offline en _tmp
    # Lee _tmp, intenta enviar al server.
    # Si OK => en conv queda RECIBIDO y se elimina del _tmp.
    pending = read_lines(tmp_path)                      # Lee todas las líneas pendientes del archivo _tmp
    if len(pending) == 0:                               # Si no hay nada pendiente
        return send_buf                                 # No cambia buffer

    remaining = []                                     # Aquí guardas lo que NO se pudo enviar (sigue pendiente)
    i = 0                                              # Índice manual (estilo “sin for”)
    while i < len(pending):                            # Recorre todas las líneas pendientes
        line = pending[i].strip()                      # Toma una línea y quita espacios/salto final

        okc, line_to_send = _convert_enviado_to_recibido(line)  # Convierte ENVIADO->RECIBIDO si aplica
        if okc:                                        # Si se pudo convertir o ya era válida
            ok, send_buf, status, err = send_record(send_sock, send_buf, line_to_send)  # Intenta enviarla al server
            if ok and status == "OK":                  # Si comunicación ok y server aceptó
                # Guardar local como RECIBIDO , confirmador por server.py
                okr, o, d, ts, st, tsst, msg = parse_record(line_to_send)  # Parse de la línea enviada
                if okr:                                # Si parseó bien
                    merge_record(conv_path, o + ";" + d + ";" + ts + ";RECIBIDO;" + timestamp_now() + ";" + msg)
                    # Guarda en conversación local el registro como RECIBIDO (y marca tsst ahora)
            else:
                # Sigue pendiente
                remaining.append(line)                 # No se pudo enviar => se mantiene en _tmp
        else:
            remaining.append(line)                     # Si la línea era inválida, también la conservas

        i = i + 1                                     # Avanza al siguiente pendiente

    write_lines(tmp_path, remaining)                   # Sobrescribe el _tmp con solo lo que quedó pendiente
    return send_buf                                    # Devuelve el buffer actualizado
