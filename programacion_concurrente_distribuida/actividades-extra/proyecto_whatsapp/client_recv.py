import time  # Para hacer pausas (sleep) y controlar el “polling” del loop receptor
import os    # Para comprobar si existe un archivo (tmp) y trabajar con rutas

from protocol import timestamp_now, socket_send_line, socket_recv_line, header_count, parse_record
# timestamp_now(): genera un timestamp en formato que usa tu protocolo
# socket_send_line(): envía una línea (string) por socket según tu protocolo (probablemente con \n)
# socket_recv_line(): recibe una línea, devolviendo ok + línea + buffer restante
# header_count(): interpreta el “header” para saber cuántas líneas vienen después
# parse_record(): parsea una línea de mensaje con formato "origen;destino;ts;estado;tsst;msg"

from storage import list_local_peers, last_timestamp, merge_record
# list_local_peers(): lista usuarios (peers) detectados en la carpeta local del usuario
# last_timestamp(): saca el último timestamp guardado en una conversación local (para pedir UPDATE incremental)
# merge_record(): añade un registro al archivo de conversación, evitando duplicados o manteniendo orden

from client_send import connect_port, flush_tmp_for_peer
# connect_port(): conecta a un puerto del servidor (send o recv) y hace autenticación, devuelve socket+buffer
# flush_tmp_for_peer(): reenvía al servidor lo guardado en _tmp y lo mezcla/actualiza en conversación

def set_offline(shared):                 # Pone el cliente en modo offline y cierra sockets de forma segura
    lock = shared["lock"]                # Obtiene el Lock compartido
    lock.acquire()                       # Entra en sección crítica

    shared["online"] = False             # Marca como offline

    if shared["send_sock"]:              # Si había socket de envío
        try:
            shared["send_sock"].close()  # Intenta cerrarlo
        except:
            pass                         # Si falla, ignora
    if shared["recv_sock"]:              # Si había socket de recepción
        try:
            shared["recv_sock"].close()  # Intenta cerrarlo
        except:
            pass                         # Ignora errores

    shared["send_sock"] = None           # Limpia referencia del socket envío
    shared["recv_sock"] = None           # Limpia referencia del socket recepción
    shared["send_buf"] = b""             # Resetea buffer de envío del protocolo
    shared["recv_buf"] = b""             # Resetea buffer de recepción del protocolo

    lock.release()                       # Sale de la sección crítica

def try_reconnect(shared, cfg):  # Intenta reconectar: abre el socket de envío y el de recepción al servidor
    okS, send_sock, send_buf = connect_port(cfg["ip"], cfg["port_send"], cfg["timeout"], cfg["user"], cfg["pwd"])
    # Conecta al puerto de envío: devuelve si ok, socket y buffer inicial
    if not okS:                  # Si no pudo conectar el canal de envío
        return False             # No se reconectó

    okR, recv_sock, recv_buf = connect_port(cfg["ip"], cfg["port_recv"], cfg["timeout"], cfg["user"], cfg["pwd"])
    # Conecta al puerto de recepción
    if not okR:                  # Si falla el canal de recepción
        try:
            send_sock.close()    # Cierra el canal de envío que ya abriste (limpieza)
        except:
            pass
        return False             # No se reconectó

    lock = shared["lock"]        # Lock para actualizar estado compartido
    lock.acquire()               # Sección crítica
    shared["online"] = True      # Ya estamos online
    shared["send_sock"] = send_sock  # Guarda socket envío
    shared["recv_sock"] = recv_sock  # Guarda socket recepción
    shared["send_buf"] = send_buf    # Guarda buffer envío
    shared["recv_buf"] = recv_buf    # Guarda buffer recepción
    lock.release()               # Sale
    return True                  # Reconexión exitosa

def flush_all_tmp(shared, cfg):         # Envía al servidor todos los mensajes guardados en _tmp (offline)
    lock = shared["lock"]               # Lock
    lock.acquire()                      # Sección crítica para copiar estado
    send_sock = shared["send_sock"]     # Socket envío
    send_buf = shared["send_buf"]       # Buffer envío
    online = shared["online"]           # Estado online
    lock.release()                      # Salimos

    if not online or send_sock is None: # Si no hay conexión real
        return                          # No se puede flushear nada

    for peer in list_local_peers(cfg["user_dir"], cfg["user"]):  # Recorre todos los peers locales
        tmp_path = cfg["tmp_path"](peer)                         # Ruta del archivo tmp de ese peer
        conv_path = cfg["conv_path"](peer)                       # Ruta del archivo conversación real
        if os.path.exists(tmp_path):                              # Si existe tmp (hay mensajes pendientes)
            send_buf = flush_tmp_for_peer(send_sock, send_buf, tmp_path, conv_path)
            # Reenvía líneas de tmp al servidor y actualiza conv_path según lo que se confirme

    lock.acquire()                      # Actualiza el buffer final en shared
    shared["send_buf"] = send_buf       # Guarda buffer actualizado
    lock.release()                      # Suelta

def recv_loop(shared, cfg):            # Loop del hilo receptor: reconecta, pide lista y updates periódicamente
    while True:                         # Bucle infinito del hilo
        lock = shared["lock"]           # Lock
        lock.acquire()                  # Sección crítica: leer estado actual
        online = shared["online"]       # ¿online?
        recv_sock = shared["recv_sock"] # Socket receptor
        recv_buf = shared["recv_buf"]   # Buffer receptor
        lock.release()                  # Salimos

        if not online:                  # Si estás offline
            if try_reconnect(shared, cfg):  # Intenta reconectar
                flush_all_tmp(shared, cfg)  # Si reconectó, envía todo lo que quedó en _tmp

        lock.acquire()                  # Relee estado (por si cambió tras reconectar)
        online = shared["online"]       # Estado actualizado
        recv_sock = shared["recv_sock"] # Socket actualizado
        recv_buf = shared["recv_buf"]   # Buffer actualizado
        lock.release()                  # Sale

        if online and recv_sock:        # Si ya estamos online y hay socket receptor
            ts = timestamp_now()        # Timestamp actual
            req_list = f"@{cfg['user']};@;{ts};LIST;00000000000000;\"\""
            # Construye un “registro” pidiendo LIST: lista de peers/conversaciones disponibles en servidor
            # Destino "@;" parece ser un broadcast/placeholder
            # "00000000000000" es tsst placeholder
            # "\"\"" es msg vacío

            if socket_send_line(recv_sock, req_list):  # Envía la petición LIST
                ok1, ack, recv_buf = socket_recv_line(recv_sock, recv_buf)     # Recibe ACK (OK/KO)
                ok2, header, recv_buf = socket_recv_line(recv_sock, recv_buf)  # Recibe header (cuántas líneas vienen)

                lock.acquire()              # Guarda el buffer actualizado en shared
                shared["recv_buf"] = recv_buf
                lock.release()

                if ok1 and ok2 and ack == "OK":               # Si todo correcto y el servidor respondió OK
                    for _ in range(header_count(header)):     # Lee tantas líneas como indique el header
                        okL, line, recv_buf = socket_recv_line(recv_sock, shared["recv_buf"])
                        # OJO: aquí usas shared["recv_buf"] en vez de recv_buf local (puede ser intencional o un bug)
                        lock.acquire()
                        shared["recv_buf"] = recv_buf         # Actualiza buffer compartido
                        lock.release()
                        if okL:                               # Si se recibió una línea válida
                            peer = line.split(";", 1)[0].strip().lstrip("@")
                            # Extrae el peer de la línea (toma campo 0 antes del primer ';', limpia y quita '@')
                            lock.acquire()
                            shared["unread"].setdefault(peer, 0)     # Inicializa contador no leídos si no existe
                            shared["pending"].setdefault(peer, [])   # Inicializa lista de pendientes si no existe
                            lock.release()
                            socket_send_line(recv_sock, "OK")        # Envía ACK por cada línea recibida (handshake)

            for peer in list_local_peers(cfg["user_dir"], cfg["user"]):  # Para cada conversación local existente
                last = last_timestamp(cfg["conv_path"](peer))           # Último timestamp guardado localmente
                ts2 = timestamp_now()                                   # Timestamp para esta petición
                req_up = f"@{cfg['user']};@{peer};{ts2};UPDATE;{last};\"\""
                # Petición UPDATE: “dame mensajes nuevos desde 'last' en la conversación con @peer”
                # msg vacío porque solo quieres actualizar

                if socket_send_line(recv_sock, req_up):                # Envía petición UPDATE
                    okA, ackA, recv_buf = socket_recv_line(recv_sock, recv_buf)    # Lee ACK
                    okB, header, recv_buf = socket_recv_line(recv_sock, recv_buf)  # Lee header
                    lock.acquire()
                    shared["recv_buf"] = recv_buf                       # Guarda buffer recibido
                    lock.release()

                    if okA and okB and ackA == "OK":                    # Si servidor OK
                        for _ in range(header_count(header)):           # Lee N mensajes
                            okM, mline, recv_buf = socket_recv_line(recv_sock, shared["recv_buf"])
                            # Igual que arriba: lee usando shared["recv_buf"]
                            lock.acquire()
                            shared["recv_buf"] = recv_buf               # Actualiza buffer
                            lock.release()

                            if okM:                                     # Si llegó un mensaje válido
                                merge_record(cfg["conv_path"](peer), mline)  # Guarda/mezcla el mensaje en conversación local
                                okr, o, d, mts, st, tsst, msg = parse_record(mline)  # Parse del mensaje recibido
                                if okr and d == f"@{cfg['user']}" and o == f"@{peer}":
                                    # Si es un mensaje entrante (peer -> yo)
                                    lock.acquire()
                                    shared["pending"].setdefault(peer, []).append(mline)  # Lo agrega a pendientes
                                    shared["unread"][peer] = shared["unread"].get(peer, 0) + 1  # Incrementa no leídos
                                    lock.release()
                                    socket_send_line(recv_sock, "OK")   # ACK al servidor por este mensaje
        time.sleep(cfg["poll_seconds"])  # Espera antes de volver a pedir LIST/UPDATE (polling)
