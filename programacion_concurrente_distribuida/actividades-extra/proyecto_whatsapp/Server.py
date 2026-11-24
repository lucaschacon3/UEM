import socket      # Sockets TCP (servidor)
import threading   # Hilos: un hilo por conexión + dos servidores (envío/recepción)
import os          # Archivos, directorios, listar archivos

from protocol import (  # Importa funciones de tu “protocolo” de texto por líneas
    timestamp_now, parse_login, parse_record,
    socket_send_line, socket_recv_line
)
from storage import ensure_dir, read_lines, write_lines, append_line
# ensure_dir(): crea directorio si no existe
# read_lines()/write_lines(): leer/escribir listas de líneas en archivos
# append_line(): append de una línea al archivo

SERVER_IP = "127.0.0.1"  # Servidor escucha solo en localhost (solo máquina local)

# MacOS => usamos 5500/5501 
PORT_ENVIO = 5500   # Puerto para canal “ENVIO” (clientes mandan mensajes/receipts)  (comentario dice windows 666)
PORT_RECV = 5501    # Puerto para canal “RECV”  (clientes piden LIST/UPDATE)         (comentario dice windows 999)

TIMEOUT_SEC = 10    # Timeout para operaciones de socket

USERS_FILE = "users.txt" # Archivo con usuarios y contraseñas
LOG_DIR = "logs"         # Carpeta donde se guardan conversaciones (logs)

ensure_dir(LOG_DIR)      # Asegura que existe la carpeta logs

users_lock = threading.Lock()  # Lock para proteger el diccionario users (multi-hilo)
logs_lock = threading.Lock()   # Lock para proteger accesos a archivos de logs

users = {}  # Diccionario: usuario -> contraseña


def load_users(path):               # Carga usuarios desde un archivo de texto
    data = {}                       # Diccionario temporal
    if os.path.exists(path):        # Solo si existe el archivo
        f = open(path, "r")         # Abre en modo lectura
        lines = f.readlines()       # Lee todas las líneas
        f.close()                   # Cierra

        i = 0
        while i < len(lines):       # Recorre líneas manualmente
            line = lines[i].strip() # Quita espacios y \n
            if line != "":          # Ignora líneas vacías
                # Acepta "user;pwd" o "user:pwd" por si acaso
                if ";" in line:                 # Si usa ';' como separador
                    parts = line.split(";")     # Divide por ';'
                else:                            # Si no, asume ':'
                    parts = line.split(":")     # Divide por ':'

                if len(parts) == 2:             # Deben ser exactamente usuario y password
                    u = parts[0].strip()        # Usuario
                    p = parts[1].strip()        # Password
                    if u != "" and p != "":     # Si ambos no vacíos
                        data[u] = p             # Guarda en dict
            i = i + 1                           # Siguiente línea
    return data                                 # Devuelve diccionario usuario->pwd


def auth_ok(user, pwd):            # Verifica autenticación
    users_lock.acquire()           # Lock para leer users con seguridad
    ok = (user in users) and (users[user] == pwd)  # Existe y coincide password
    users_lock.release()           # Suelta lock
    return ok                      # Devuelve True/False


def user_exists(user):             # Comprueba si existe un usuario
    users_lock.acquire()           # Lock
    ok = (user in users)           # True si está en el diccionario
    users_lock.release()           # Suelta
    return ok                      # Devuelve True/False


def conv_file(u1, u2):             # Devuelve el archivo de conversación para el par (u1, u2)
    f1 = LOG_DIR + "/" + u1 + "_" + u2 + ".txt"  # Opción 1: u1_u2
    f2 = LOG_DIR + "/" + u2 + "_" + u1 + ".txt"  # Opción 2: u2_u1 (el orden inverso)

    if os.path.exists(f1):         # Si ya existe con orden u1_u2
        return f1                  # Usa ese
    if os.path.exists(f2):         # Si existe con orden u2_u1
        return f2                  # Usa ese

    # nueva conversación: la crea con el orden del primer emisor u1->u2
    f = open(f1, "a")              # Crea el archivo vacío (append)
    f.close()                      # Cierra
    return f1                      # Devuelve el nuevo path


def update_state_in_file(path, origin_at, dest_at, ts, msg_field, new_state, new_ts_state):
    # Actualiza el estado (RECIBIDO/ENTREGADO/LEIDO/...) de un mensaje concreto dentro del log
    logs_lock.acquire()            # Lock global de logs (evita escrituras concurrentes)
    lines = read_lines(path)       # Lee todas las líneas del log
    out = []                       # Salida reescrita

    i = 0
    while i < len(lines):          # Recorre línea por línea
        ok, o, d, lts, st, tsst, msg = parse_record(lines[i])  # Parsea la línea
        if ok and o == origin_at and d == dest_at and lts == ts and msg == msg_field:
            # Si coincide exactamente (origen, destino, timestamp, y mensaje)
            out.append(o + ";" + d + ";" + lts + ";" + new_state + ";" + new_ts_state + ";" + msg)
            # Reemplaza esa línea por otra con nuevo estado y timestamp de estado
        else:
            out.append(lines[i])   # Si no coincide, deja la línea tal cual
        i = i + 1                  # Siguiente

    write_lines(path, out)         # Sobrescribe el archivo con el contenido actualizado
    logs_lock.release()            # Suelta lock


def list_conversations_for(user):  # Devuelve lista de peers y cuántos mensajes RECIBIDO pendientes tiene user
    peers = {}                     # peer -> contador de "RECIBIDO" hacia user
    logs_lock.acquire()            # Bloquea acceso a logs
    files = os.listdir(LOG_DIR)    # Lista archivos en logs/

    i = 0
    while i < len(files):          # Recorre cada archivo
        name = files[i]
        if name.endswith(".txt"):  # Solo archivos .txt
            path = LOG_DIR + "/" + name          # Path completo
            lines = read_lines(path)             # Lee líneas del archivo

            j = 0
            while j < len(lines):                # Recorre líneas del archivo
                ok, o, d, ts, st, tsst, msg = parse_record(lines[j])  # Parsea registro
                if ok:                           # Solo si parse correcto
                    ou = o[1:]                   # Usuario origen sin '@'
                    du = d[1:]                   # Usuario destino sin '@'
                    if ou == user or du == user: # Si el archivo contiene mensajes del user
                        peer = ou                # Candidato peer = origen
                        if peer == user:         # Si el origen es el mismo user
                            peer = du            # entonces el peer es el destino
                        if peer != "":           # Evita vacío
                            if peer not in peers:
                                peers[peer] = 0  # Inicializa contador
                            if du == user and st == "RECIBIDO":
                                peers[peer] = peers[peer] + 1  # Cuenta pendientes RECIBIDO hacia user
                j = j + 1
        i = i + 1

    logs_lock.release()            # Suelta lock logs

    res = []                       # Lista final (peer, contador)
    for k in peers:
        res.append((k, peers[k]))  # Convierte dict a lista de tuplas
    res.sort(key=lambda x: x[0])   # Ordena alfabéticamente por peer
    return res                     # Devuelve lista


def send_block(conn, header_line, lines):
    # Envía un “bloque”: primero OK + header, luego espera OK del cliente, luego manda N líneas con ACK por línea

    socket_send_line(conn, "OK")         # 1) “OK” inicial del servidor
    socket_send_line(conn, header_line)  # 2) Envía la cabecera (incluye conteo en el campo mensaje)

    buf = b""                            # Buffer de recepción local para este intercambio
    ok, ack, buf = socket_recv_line(conn, buf)  # 3) Espera ACK del cliente (debe ser "OK")

    if ok and ack == "OK":               # Si el cliente confirmó
        i = 0
        sending = True                   # Bandera para cortar envío si algo falla
        while i < len(lines) and sending: # Envía cada línea del bloque
            okS = socket_send_line(conn, lines[i])  # Envía una línea
            if okS:
                ok2, ack2, buf = socket_recv_line(conn, buf)  # Espera ACK por esa línea
                if ok2:
                    if ack2 != "OK":     # Si el ACK no es OK, detiene
                        sending = False
                else:
                    sending = False      # Si no pudo leer ACK, detiene
            else:
                sending = False          # Si no pudo enviar, detiene
            i = i + 1                   # Siguiente línea


def handle_envio(conn, addr):            # Handler del puerto ENVIO (mensajes y receipts)
    conn.settimeout(TIMEOUT_SEC)         # Configura timeout en la conexión
    buf = b""                            # Buffer para socket_recv_line

    ok, line, buf = socket_recv_line(conn, buf)  # Espera primera línea (LOGIN:...)
    if not ok:
        conn.close()                     # Si falla, cierra conexión
        return                           # Sale del handler

    okL, user, pwd = parse_login(line)   # Parsea login
    if not (okL and auth_ok(user, pwd)): # Si login inválido o auth falla
        socket_send_line(conn, "KO")     # Responde KO
        conn.close()                     # Cierra
        return                           # Sale

    socket_send_line(conn, "OK")         # Login correcto

    running = True                       # Control del loop
    while running:
        ok2, msg, buf = socket_recv_line(conn, buf)  # Recibe siguiente mensaje/línea del cliente
        if ok2:
            if msg == "FIN":             # El cliente quiere cerrar sesión
                socket_send_line(conn, "OK")  # Confirma cierre
                running = False               # Sale del bucle

            elif msg.startswith("EXISTS:"):   # Petición EXISTS del cliente
                target = msg.split(":", 1)[1].strip()  # Extrae target_user
                if user_exists(target):       # Si el usuario existe
                    socket_send_line(conn, "OK")
                else:
                    socket_send_line(conn, "KO")

            else:
                okr, o, d, ts, st, tsst, m = parse_record(msg)  # Intenta parsear registro normal
                if okr:
                    origin_user = o[1:]         # Origen sin '@'
                    dest_user = d[1:]           # Destino sin '@'

                    # Seguridad: el origin del record debe coincidir con el usuario logueado
                    if origin_user != user:     # Si el cliente intenta falsificar el origen
                        socket_send_line(conn, "OK")  # Ignora (pero responde OK para no romper protocolo)
                    else:
                        # 1) ENVÍO DE MENSAJE
                        if st == "ENVIADO" or st == "RECIBIDO":  # Estados que significan “mensaje enviado”
                            if not user_exists(dest_user):       # Si destino no existe
                                socket_send_line(conn, "KO")     # Responde KO
                                err = o + ";" + d + ";" + ts + ";ERROR;00000000000000;\"Usuario no registrado.\""
                                socket_send_line(conn, err)      # Envía línea extra de error (según tu mini-protocolo)
                                ok3, ack, buf = socket_recv_line(conn, buf)  # Espera ACK del cliente
                            else:
                                socket_send_line(conn, "OK")     # Destino existe => OK
                                file_path = conv_file(origin_user, dest_user)  # Archivo de conversación
                                server_ts = timestamp_now()      # Timestamp del servidor para marcar “RECIBIDO”
                                logs_lock.acquire()              # Bloquea logs
                                append_line(file_path, o + ";" + d + ";" + ts + ";RECIBIDO;" + server_ts + ";" + m)
                                # Guarda el mensaje como RECIBIDO (en logs del server)
                                logs_lock.release()              # Suelta logs

                        # 2) RECEIPT LEIDO
                        elif st == "LEIDO":              # Cliente está marcando un mensaje como leído
                            socket_send_line(conn, "OK") # Acepta
                            file_path = conv_file(origin_user, dest_user)  # Archivo de conversación
                            new_ts = tsst                # Timestamp estado recibido del cliente
                            if new_ts == "" or new_ts == "00000000000000":
                                new_ts = timestamp_now() # Si viene vacío/placeholder, el server pone su timestamp
                            update_state_in_file(file_path, o, d, ts, m, "LEIDO", new_ts)  # Actualiza el estado en el log

                        else:
                            socket_send_line(conn, "OK") # Cualquier otro estado: lo ignora pero responde OK
                else:
                    socket_send_line(conn, "OK")         # Si no parsea, responde OK para mantener el flujo
        else:
            running = False                              # Si falla recv_line, termina loop

    conn.close()                                         # Cierra conexión al salir


def handle_recepcion(conn, addr):         # Handler del puerto RECV (LIST / UPDATE)
    conn.settimeout(TIMEOUT_SEC)          # Timeout
    buf = b""                             # Buffer

    ok, line, buf = socket_recv_line(conn, buf)  # Lee LOGIN
    if not ok:
        conn.close()
        return

    okL, user, pwd = parse_login(line)    # Parsea login
    if not (okL and auth_ok(user, pwd)):  # Auth
        socket_send_line(conn, "KO")
        conn.close()
        return

    socket_send_line(conn, "OK")          # Login OK

    running = True
    while running:
        ok2, req, buf = socket_recv_line(conn, buf)  # Lee request
        if ok2:
            if req == "FIN":              # Cierre
                socket_send_line(conn, "OK")
                running = False
            else:
                parts = req.split(";", 5) # Interpreta request en formato record (6 campos)
                if len(parts) == 6:
                    origin = parts[0].strip()  # Origen (debe ser @user)
                    dest = parts[1].strip()    # Destino (peer o @;)
                    ts = parts[2].strip()      # Timestamp de la request
                    cmd = parts[3].strip()     # Comando LIST/UPDATE
                    last_ts = parts[4].strip() # Timestamp “desde” para UPDATE

                    if origin == ("@" + user): # Seguridad: request debe venir “firmada” como @user
                        if cmd == "LIST":      # LIST: devolver peers + pendientes
                            convs = list_conversations_for(user)  # Lista (peer, pendientes RECIBIDO)
                            header = origin + ";@;" + ts + ";LIST;00000000000000;\"" + str(len(convs)) + "\""
                            # Header: en el campo mensaje llevas "N" = número de líneas

                            lines = []         # Líneas del bloque LIST
                            i = 0
                            while i < len(convs):
                                peer, pending = convs[i]
                                lines.append("@" + peer + ";@" + user + ";00000000000000;LIST;00000000000000;\"" + str(pending) + "\"")
                                # Cada línea lista el peer y cuántos RECIBIDO pendientes tiene
                                i = i + 1

                            send_block(conn, header, lines)  # Envía bloque con handshake

                        elif cmd == "UPDATE":  # UPDATE: devolver nuevos mensajes/cambios desde last_ts
                            peer = dest[1:] if dest.startswith("@") else dest  # Obtiene peer sin '@'
                            file_path = conv_file(user, peer)                  # Archivo conversación

                            logs_lock.acquire()
                            all_lines = read_lines(file_path)                  # Lee todo el archivo
                            logs_lock.release()

                            out_lines = []     # Líneas que se enviarán al cliente como “actualización”
                            rewritten = []     # Líneas para reescribir en el archivo (cambiando estados si aplica)

                            i = 0
                            while i < len(all_lines):
                                okr, o, d, mts, st, tsst, m = parse_record(all_lines[i])  # Parse de línea del log
                                if okr:
                                    ou = o[1:]  # origen sin '@'
                                    du = d[1:]  # destino sin '@'
                                    same_pair = ((ou == user and du == peer) or (ou == peer and du == user))
                                    # same_pair = la línea pertenece a esa conversación user<->peer

                                    # IMPORTANTE: usamos >= para enviar cambios de estado en mismo timestamp
                                    if same_pair and mts >= last_ts:  # Si está en el rango de actualización
                                        if du == user and st == "RECIBIDO":  # Si es mensaje hacia el user aún “RECIBIDO”
                                            new_ts_state = timestamp_now()   # El server marca momento de entrega
                                            st2 = "ENTREGADO"                # Cambia estado a ENTREGADO
                                            tsst2 = new_ts_state             # Timestamp de estado “entregado”
                                            new_line = o + ";" + d + ";" + mts + ";" + st2 + ";" + tsst2 + ";" + m
                                            out_lines.append(new_line)       # Lo envía al cliente como actualización
                                            rewritten.append(new_line)       # Y lo reescribe en el log con ENTREGADO
                                        else:
                                            out_lines.append(o + ";" + d + ";" + mts + ";" + st + ";" + tsst + ";" + m)
                                            rewritten.append(all_lines[i])   # No cambia nada en el log
                                    else:
                                        rewritten.append(all_lines[i])       # Fuera de rango => se mantiene
                                else:
                                    rewritten.append(all_lines[i])           # Línea inválida => se mantiene

                                i = i + 1

                            logs_lock.acquire()
                            write_lines(file_path, rewritten)                 # Reescribe el log con cambios (RECIBIDO->ENTREGADO)
                            logs_lock.release()

                            header = origin + ";@" + peer + ";" + ts + ";UPDATE;" + last_ts + ";\"" + str(len(out_lines)) + "\""
                            # Header UPDATE con número de líneas a enviar
                            send_block(conn, header, out_lines)               # Envía bloque UPDATE
        else:
            running = False  # Si socket_recv_line falla, termina

    conn.close()             # Cierra conexión


def start_server(port, handler):                 # Inicia un servidor TCP en un puerto con un handler por conexión
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reutilizar dirección/puerto rápido al reiniciar
    s.bind((SERVER_IP, port))                      # Bind a localhost:port
    s.listen()                                     # Empieza a escuchar

    running = True
    while running:
        conn, addr = s.accept()                    # Acepta una conexión entrante (bloqueante)
        t = threading.Thread(target=handler, args=(conn, addr))  # Crea hilo para manejarla
        t.start()                                  # Arranca el hilo handler


users = load_users(USERS_FILE)  # Carga users.txt al iniciar el servidor
print("Servidor OK:", SERVER_IP, "ENVIO", PORT_ENVIO, "RECV", PORT_RECV)  # Log de arranque

threading.Thread(target=start_server, args=(PORT_ENVIO, handle_envio)).start()
# Lanza un hilo servidor para el puerto de ENVIO

threading.Thread(target=start_server, args=(PORT_RECV, handle_recepcion)).start()
# Lanza un hilo servidor para el puerto de RECEPCION
