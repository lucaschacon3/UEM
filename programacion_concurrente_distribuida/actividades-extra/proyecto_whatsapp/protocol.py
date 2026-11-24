import time  # Módulo para trabajar con tiempo y formatear fechas/horas


def timestamp_now():  # Devuelve un timestamp “compacto” como string
    return time.strftime("%Y%m%d%H%M%S")  # Formato: AAAAMMDDHHMMSS (ej: 20260106184530)


def parse_login(line):  # Parsea una línea de login del tipo "LOGIN:USUARIO:CONTRASEÑA"
    # LOGIN:USUARIO:CONTRASEÑA
    ok = False          # Bandera: por defecto asumimos que NO es válido
    usuario = ""        # Resultado usuario por defecto vacío
    clave = ""          # Resultado clave por defecto vacío
    if line.startswith("LOGIN"):         # Comprueba que la línea empieza con "LOGIN" (no exige "LOGIN:")
        partes = line.split(":")         # Separa por ":" -> ["LOGIN", "USUARIO", "CONTRASEÑA"]
        if len(partes) == 3:             # Debe haber exactamente 3 partes
            usuario = partes[1].strip()  # Usuario es la parte 1, limpiando espacios
            clave = partes[2].strip()    # Clave es la parte 2, limpiando espacios
            ok = True                    # Marcamos parse correcto
    return ok, usuario, clave            # Devuelve si ok y los campos (aunque sean vacíos)


def parse_record(line):  # Parsea un registro de chat con 6 campos separados por ';'
    # @ORIGEN;@DESTINO;TS;ESTADO;TS_ESTADO;"MENSAJE"
    partes = line.split(";", 5)          # Divide en máximo 6 trozos (5 splits), para que el mensaje pueda tener ';'
    if len(partes) != 6:                # Si no quedan exactamente 6 partes, formato inválido
        return False, "", "", "", "", "", ""  # Devuelve fallo y campos vacíos

    origen = partes[0].strip()          # Campo 0: origen (ej "@gino")
    destino = partes[1].strip()         # Campo 1: destino (ej "@pepe")
    ts = partes[2].strip()              # Campo 2: timestamp principal
    estado = partes[3].strip()          # Campo 3: estado (ENVIADO/RECIBIDO/LEIDO/...)
    ts_estado = partes[4].strip()       # Campo 4: timestamp del estado (cuándo se entregó/leyó)
    mensaje = partes[5].strip()         # Campo 5: mensaje (normalmente entre comillas)

    if not origen.startswith("@"):      # Validación básica: origen debe empezar por '@'
        return False, "", "", "", "", "", ""
    if not destino.startswith("@"):     # Validación básica: destino debe empezar por '@'
        return False, "", "", "", "", "", ""

    return True, origen, destino, ts, estado, ts_estado, mensaje  # Devuelve parse correcto


def socket_send_line(sock, text):  # Envía un string como “línea” (terminada en '\n') por un socket
    ok = True                      # Asume éxito
    try:
        sock.send((text + "\n").encode())  # Envía bytes con salto de línea al final (framing por '\n')
    except Exception:
        ok = False                 # Si falla, marca ok False
    return ok                      # Devuelve si se envió correctamente


def socket_recv_line(sock, buffer_bytes):  # Recibe 1 línea terminada en '\n', usando buffer acumulado
    ok = True                      # Bandera de éxito
    line = ""                      # Línea resultante (string)
    data = buffer_bytes            # data empieza con lo que ya teníamos en buffer
    found = False                  # Indica si encontramos '\n'
    running = True                 # Control del bucle de recepción

    while running:                 # Bucle hasta encontrar '\n' o fallar
        pos = data.find(b"\n")     # Busca el primer '\n' en el buffer actual
        if pos != -1:              # Si encontramos '\n'
            head = data[:pos]      # head: bytes antes del '\n' (la línea)
            rest = data[pos + 1:]  # rest: bytes después del '\n' (lo que sobra para la próxima llamada)
            try:
                line = head.decode()  # Decodifica bytes a string (utf-8 por defecto)
            except Exception:
                line = ""          # Si falla decodificación, deja línea vacía
                ok = False         # Marca error
            data = rest            # Actualiza buffer restante
            found = True           # Marcamos que encontramos una línea completa
            running = False        # Salimos del bucle
        else:                      # Si NO hay '\n' aún, necesitamos leer más del socket
            chunk = b""            # Trozo leído del socket
            try:
                chunk = sock.recv(4096)  # Lee hasta 4096 bytes (bloquea hasta recibir o timeout/cierre)
            except Exception:
                chunk = b""        # Si hay excepción (timeout/error), simula “no llegó nada”
            if chunk:              # Si llegó contenido
                data = data + chunk  # Lo añade al buffer acumulado
            else:                  # Si no llegó nada (socket cerrado o error)
                ok = False         # Marca fallo
                running = False    # Sale del bucle

    if (not found) and ok:         # Si no se encontró línea completa pero “ok” seguía True
        ok = False                 # Fuerza ok False: no se puede devolver línea sin '\n'

    return ok, line, data          # Devuelve: si ok, la línea, y el buffer restante


def header_count(header_line):     # Extrae un número N desde un “header” con formato de record (campo 6 = "N")
    partes = header_line.split(";", 5)  # Parte header como si fuera un record con 6 campos
    n = 0                               # Por defecto 0
    if len(partes) == 6:                # Deben existir 6 partes
        txt = partes[5].strip()         # Toma el campo mensaje (parte 5)
        if len(txt) >= 2 and txt[0] == "\"" and txt[-1] == "\"":  # Debe venir entre comillas: "123"
            num = txt[1:-1]             # Quita comillas => 123
            if num.isdigit():           # Comprueba que solo son dígitos
                n = int(num)            # Convierte a entero
    return n                            # Retorna el contador
