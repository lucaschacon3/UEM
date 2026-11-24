import threading  # Librería para crear hilos (thread) y usar Locks (bloqueos)
import os         # Librería para trabajar con rutas, archivos, y comprobar si existen

from protocol import timestamp_now, parse_record  # Funciones del “protocolo”: obtener timestamp y parsear registros
from storage import ensure_dir, merge_record, read_lines, list_local_peers, mark_delivered_to_read  # Operaciones de almacenamiento local
from client_send import send_record, send_fin, send_exists  # Envío al servidor: mensajes, fin de sesión, preguntar si existe usuario
from client_recv import recv_loop, set_offline  # Hilo receptor + función para marcar estado offline

CFG = {  # Configuración de red del cliente
    "ip": "127.0.0.1",      # IP del servidor (localhost)
    "port_send": 5500,      # Puerto al que este cliente envía
    "port_recv": 5501,      # Puerto por el que este cliente recibe (o donde escucha el servidor para este canal)
    "timeout": 10,          # Timeout de sockets (segundos)
    "poll_seconds": 5       # Cada cuánto reintentar / hacer polling en el loop receptor
}

BASE_DIR = "client_data"            # Carpeta base donde se guardan conversaciones por usuario
RESERVED = ["lista", "salir"]       # Comandos reservados (no permitidos como nombre de usuario)

def build_paths(user_dir, user):    # Construye funciones para calcular rutas de archivos según usuario y peer
    def conv_path(peer):            # Devuelve ruta del archivo “conversación” con peer
        return user_dir + "/" + user + "_" + peer + ".txt"  # Ej: client_data/gino/gino_pepe.txt
    def tmp_path(peer):             # Devuelve ruta del archivo temporal (mensajes offline pendientes)
        return user_dir + "/" + user + "_" + peer + "_tmp.txt"  # Ej: .../gino_pepe_tmp.txt
    return conv_path, tmp_path      # Retorna ambas funciones (closures) para usarlas luego

def is_valid_username(name):        # Valida si un nombre de usuario cumple reglas mínimas
    if name is None:                # Si no hay nombre
        return False                # No es válido
    u = name.strip()                # Quita espacios al inicio/final
    if u == "" or u.startswith("@") or ";" in u or ":" in u or " " in u:  # Reglas de caracteres prohibidos
        return False                # No es válido
    if u.lower() in RESERVED:       # Si coincide con comando reservado (lista/salir)
        return False                # No es válido
    return all(ch.isalnum() or ch in "_-" for ch in u)  # Solo alfanumérico, "_" o "-"

def print_conversation(path, max_lines=100):  # Imprime la conversación (últimas max_lines líneas)
    lines = read_lines(path)                  # Lee todas las líneas del archivo
    for line in lines[-max_lines:]:           # Recorre solo las últimas max_lines
        ok, o, d, ts, st, tsst, msg = parse_record(line)  # Parseo: origen, destino, timestamp, estado, etc.
        if ok:                                # Si el parseo fue correcto
            if msg.startswith('"') and msg.endswith('"'):  # Si el msg viene entre comillas
                msg = msg[1:-1]               # Quita las comillas exteriores
            print(ts, o + ":", msg)           # Imprime “timestamp @origen: mensaje”

def pull_pending_and_refresh(shared, peer):  # “Resetea” pendientes y contadores de no-leídos para ese peer
    lock = shared["lock"]                     # Obtiene el Lock compartido (para proteger datos)
    lock.acquire()                            # Entra en sección crítica
    shared["pending"][peer] = []              # Reinicia la lista de mensajes pendientes para ese peer
    shared["unread"][peer] = 0                # Reinicia contador de no-leídos
    lock.release()                            # Sale de sección crítica

def send_read_receipts(shared, receipts):     # Envía “recibos de lectura” al servidor si está online
    lock = shared["lock"]                     # Lock para acceder a shared
    lock.acquire()                            # Sección crítica (leer estado actual)
    online = shared["online"]                 # Estado: conectado o no
    send_sock = shared["send_sock"]           # Socket de envío (si existe)
    send_buf = shared["send_buf"]             # Buffer acumulado (por tu protocolo)
    lock.release()                            # Suelta lock (ya copiamos lo necesario)

    if online and send_sock:                  # Solo si estamos online y tenemos socket válido
        all_ok = True                         # Asume que todo va bien
        for receipt in receipts:              # Recorre cada recibo (cada “registro” de confirmación)
            ok, send_buf, status, err = send_record(send_sock, send_buf, receipt)  # Envía recibo
            if not ok:                        # Si hubo fallo de comunicación
                all_ok = False                # Marcamos que no fue todo ok
        lock.acquire()                        # Vuelve a lock para actualizar shared
        shared["send_buf"] = send_buf         # Guarda el buffer actualizado
        lock.release()                        # Suelta lock
        if not all_ok:                        # Si algo falló
            set_offline(shared)               # Marca offline (para que el sistema reintente luego)

def server_user_exists_if_online(shared, target_user):  # Pregunta al servidor si existe el usuario target
    lock = shared["lock"]                     # Lock para leer estado
    lock.acquire()                            # Sección crítica
    online = shared["online"]                 # ¿estamos online?
    send_sock = shared["send_sock"]           # Socket de envío
    send_buf = shared["send_buf"]             # Buffer de envío
    lock.release()                            # Salimos

    if not online or not send_sock:           # Si no estamos online o no hay socket
        return False, False, send_buf         # (no se preguntó, no existe/unknown, buffer actual)

    ok_comm, send_buf, exists = send_exists(send_sock, send_buf, target_user)  # Consulta “exists” al servidor
    lock.acquire()                            # Actualiza shared con el buffer nuevo
    shared["send_buf"] = send_buf             # Guarda buffer actualizado
    lock.release()                            # Suelta
    if not ok_comm:                           # Si la comunicación falló
        set_offline(shared)                   # Se marca offline
    return True, exists, send_buf             # (sí se preguntó, existe o no, buffer final)

def can_open_chat(shared, user_dir, usuario, conv_path, target_user):  # Decide si se permite abrir chat con target_user
    if not is_valid_username(target_user):    # Valida nombre objetivo
        return False, "Error: nombre de usuario inválido"  # Rechaza
    if target_user == usuario:                # No permitas hablar contigo mismo
        return False, "Error: no puedes chatear contigo mismo"  # Rechaza

    asked, exists, _ = server_user_exists_if_online(shared, target_user)  # Si online, pregunta al servidor
    if asked:                                 # Si se pudo preguntar
        if not exists:                        # Si el servidor dice que no existe
            return False, "Error: el usuario @" + target_user + " no existe en el servidor"  # Rechaza
        return True, ""                       # Existe => se puede abrir chat

    path = conv_path(target_user)             # Ruta del archivo local de conversación con ese user
    if os.path.exists(path) or target_user in list_local_peers(user_dir, usuario):  # Si ya existe conversación local
        return True, ""                       # Se permite abrir (aunque estés offline)

    return False, "(OFFLINE) No puedes iniciar un chat nuevo. Conéctate al servidor y prueba otra vez."  # Offline y no hay historial

def main():                                   # Función principal del programa
    print("=== Console Whatsapp (MAC) ===")    # Banner del programa
    usuario = input("Usuario: ").strip()      # Lee usuario y quita espacios
    clave = input("Contraseña: ").strip()     # Lee contraseña y quita espacios

    ensure_dir(BASE_DIR)                      # Crea carpeta base si no existe
    user_dir = BASE_DIR + "/" + usuario       # Carpeta específica del usuario
    ensure_dir(user_dir)                      # Crea carpeta del usuario si no existe

    conv_path, tmp_path = build_paths(user_dir, usuario)  # Genera funciones para construir rutas por peer

    shared = {                                # Estado compartido entre hilo principal y el hilo receptor
        "lock": threading.Lock(),             # Lock para proteger acceso concurrente
        "online": False,                      # Estado inicial: offline hasta conectar
        "send_sock": None,                    # Socket de envío (se asignará al conectar)
        "recv_sock": None,                    # Socket de recepción (se asignará al conectar)
        "send_buf": b"",                      # Buffer de envío (bytes) para tu protocolo
        "recv_buf": b"",                      # Buffer de recepción (bytes) para tu protocolo
        "unread": {},                         # Mapa peer -> número de no leídos
        "pending": {}                         # Mapa peer -> lista de pendientes (por ejemplo, mensajes por mostrar/gestionar)
    }

    recv_cfg = {                              # Config del hilo receptor
        "ip": CFG["ip"],                      # IP servidor
        "port_send": CFG["port_send"],        # Puerto envío
        "port_recv": CFG["port_recv"],        # Puerto recepción
        "timeout": CFG["timeout"],            # Timeout
        "poll_seconds": CFG["poll_seconds"],  # Polling
        "user": usuario,                      # Usuario
        "pwd": clave,                         # Password
        "user_dir": user_dir,                 # Carpeta local del usuario
        "conv_path": conv_path,               # Función para ruta conversación
        "tmp_path": tmp_path                  # Función para ruta temporal offline
    }

    t = threading.Thread(target=recv_loop, args=(shared, recv_cfg))  # Crea hilo receptor ejecutando recv_loop(shared, recv_cfg)
    t.daemon = True                           # Hilo daemon: se cierra automáticamente si termina el hilo principal
    t.start()                                 # Arranca el hilo receptor

    peers = list_local_peers(user_dir, usuario)  # Lista peers detectados por archivos locales
    chat_actual = peers[0] if peers else "?"     # Si hay peers, selecciona el primero; si no, “?”
    if chat_actual == "?":                       # Si no hay chats existentes
        print("No hay conversaciones aún. Escribe @NombreUsuario para empezar.")  # Instrucción al usuario

    running = True                            # Control del bucle principal
    while running:                            # Loop principal de la consola
        entrada = input("@" + chat_actual + ": ")  # Prompt: indica a quién estás hablando
        if entrada.startswith("@"):            # Si empieza con @ => es comando / cambio de chat
            cmd = entrada.strip()              # Limpia espacios
            if cmd == "@salir":                # Comando de salida
                lock = shared["lock"]          # Lock
                lock.acquire()                 # Sección crítica: copiar estado actual
                online = shared["online"]      # ¿online?
                send_sock = shared["send_sock"]# Socket envío
                send_buf = shared["send_buf"]  # Buffer envío
                recv_sock = shared["recv_sock"]# Socket recepción
                recv_buf = shared["recv_buf"]  # Buffer recepción
                lock.release()                 # Salimos

                if online and send_sock:       # Si online, cierra “bien” el canal de envío
                    send_buf = send_fin(send_sock, send_buf)  # Envía FIN por protocolo (cierre)
                    try:                       # Intenta cerrar socket
                        send_sock.close()      # Cierra
                    except:                    # Si falla (excepción), ignora
                        pass
                if online and recv_sock:       # Si online, cierra “bien” el canal de recepción
                    from protocol import socket_send_line, socket_recv_line  # Helpers de protocolo (líneas)
                    socket_send_line(recv_sock, "FIN")         # Envía FIN por el socket receptor
                    _, _, recv_buf = socket_recv_line(recv_sock, recv_buf)  # Espera respuesta/ack (según tu protocolo)
                    try:                       # Intenta cerrar socket
                        recv_sock.close()      # Cierra
                    except:                    # Ignora errores al cerrar
                        pass
                print("FIN DEL PROGRAMA!")     # Mensaje de salida
                running = False                # Termina el loop principal
            elif cmd == "@lista":              # Comando para listar conversaciones locales
                peers = list_local_peers(user_dir, usuario)  # Vuelve a cargar peers
                print("\n=== Conversaciones ===")            # Encabezado
                for i, peer in enumerate(peers, 1):          # Lista numerada
                    if is_valid_username(peer):              # Solo muestra nombres válidos
                        count = shared["unread"].get(peer, 0)  # No leídos (sin lock: puede ser aceptable si toleras carreras)
                        print(f"{i}- @{peer}" + (f" ({count})" if count else ""))  # Muestra “(n)” si hay no leídos
                print("======================\n")          # Cierre
            else:                                # Si no es salir/lista, interpretamos “@usuario” como cambiar/abrir chat
                nuevo = cmd[1:].strip()          # Quita el @ y limpia
                if nuevo == "":                  # Si quedó vacío
                    print("Error: usuario vacío")# Error
                else:
                    can, reason = can_open_chat(shared, user_dir, usuario, conv_path, nuevo)  # Verifica si se puede abrir chat
                    if not can:                  # Si no se puede
                        print(reason)            # Muestra motivo
                    else:                        # Si sí se puede
                        chat_actual = nuevo      # Cambia el chat actual
                        path = conv_path(chat_actual)  # Ruta conversación
                        if not os.path.exists(path):   # Si el archivo no existe aún
                            open(path, "a").close()    # Lo crea vacío (append + close)
                        pull_pending_and_refresh(shared, chat_actual)  # Reinicia pendientes/no leídos en memoria
                        receipts = mark_delivered_to_read(path, chat_actual, usuario, timestamp_now())  # Marca mensajes entregados como leídos y genera recibos
                        send_read_receipts(shared, receipts)           # Envía recibos al servidor si estás online
                        print("\n--- Conversación con @" + chat_actual + " ---")  # Encabezado conversación
                        print_conversation(path, 100)                  # Imprime últimas 100 líneas
                        print("---------------------------------\n")  # Separador
        else:                                       # Si NO empieza con @ => es un mensaje normal a chat_actual
            if chat_actual == "?" or chat_actual == "":  # Si aún no hay chat seleccionado
                print("Primero elige una conversación: escribe @NombreUsuario")  # Aviso
                continue                                # Vuelve al prompt (nota: tú sueles evitar continue; aquí solo lo comento)

            ts = timestamp_now()                        # Timestamp del mensaje
            origen = "@" + usuario                      # Origen con @
            destino = "@" + chat_actual                 # Destino con @
            msg = f'"{entrada}"'                        # Mensaje entre comillas (para tu protocolo/parse)
            record_envio = f"{origen};{destino};{ts};ENVIADO;00000000000000;{msg}"  # Registro “ENVIADO” con tsst placeholder

            lock = shared["lock"]                       # Lock
            lock.acquire()                              # Sección crítica: copiar estado conexión
            online = shared["online"]                   # ¿online?
            send_sock = shared["send_sock"]             # Socket envío
            send_buf = shared["send_buf"]               # Buffer envío
            lock.release()                              # Salimos

            if online and send_sock:                    # Si online, intenta enviar al servidor
                ok, send_buf, status, err = send_record(send_sock, send_buf, record_envio)  # Envía registro
                lock.acquire()                          # Actualiza buffer en shared
                shared["send_buf"] = send_buf           # Guarda buffer actualizado
                lock.release()                          # Suelta

                if ok and status == "OK":               # Si se envió y el servidor respondió OK
                    merge_record(conv_path(chat_actual), f"{origen};{destino};{ts};RECIBIDO;{timestamp_now()};{msg}")  # Guarda en local como “RECIBIDO”
                    pull_pending_and_refresh(shared, chat_actual)  # Refresca memoria de pendientes/no-leídos
                    receipts = mark_delivered_to_read(conv_path(chat_actual), chat_actual, usuario, timestamp_now())   # Marca entregado->leído
                    send_read_receipts(shared, receipts)  # Envía recibos de lectura
                    print("\n--- @" + chat_actual + " ---")  # Encabezado
                    print_conversation(conv_path(chat_actual), 100) # Reimprime conversación
                    print("-----------------\n")              # Separador
                elif ok and status == "KO" and err:      # Si el servidor respondió KO con detalle de error
                    merge_record(conv_path(chat_actual), err)  # Guarda el “registro de error” en local
                    print("Servidor ERROR:", err)             # Muestra error
                elif not ok:                                # Si falló la comunicación
                    set_offline(shared)                      # Marca offline (para que se guarde/reenvié luego)
            else:                                            # Si estás offline
                merge_record(conv_path(chat_actual), f"{origen};{destino};{ts};ENVIADO;{timestamp_now()};{msg}")  # Guarda localmente como ENVIADO
                with open(tmp_path(chat_actual), "a") as f:  # Abre archivo tmp del peer en append (pendiente de enviar)
                    f.write(f"{origen};{destino};{ts};ENVIADO;{timestamp_now()};{msg}\n")  # Escribe línea pendiente
                print("\n(OFFLINE) Guardado en _tmp. Se enviará automáticamente al reconectar.\n")  # Aviso al usuario

if __name__ == "__main__":  # Si este archivo se ejecuta directamente (no importado como módulo)
    main()                  # Llama a main()
