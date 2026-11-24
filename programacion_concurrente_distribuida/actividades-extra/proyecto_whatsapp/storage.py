import os                      # Para manejar rutas, comprobar existencia, listar directorios
from protocol import parse_record  # Para parsear líneas con formato @o;@d;ts;estado;tsst;"msg"

def ensure_dir(path):          # Asegura que un directorio exista
    if not os.path.exists(path):  # Si NO existe
        os.mkdir(path)            # Lo crea (ojo: solo crea 1 nivel, no crea padres)


def read_lines(path):          # Lee un archivo de texto y devuelve lista de líneas SIN '\n'
    if os.path.exists(path):   # Solo si el archivo existe
        f = open(path, "r")    # Abre en lectura
        lines = f.readlines()  # Lee todas las líneas en memoria
        f.close()              # Cierra archivo

        out = []               # Lista salida (sin saltos de línea)
        i = 0
        while i < len(lines):  # Recorre líneas manualmente
            out.append(lines[i].rstrip("\n"))  # Quita solo el '\n' final
            i = i + 1
        return out             # Devuelve lista de líneas
    return []                  # Si no existe, devuelve lista vacía


def write_lines(path, lines):  # Sobrescribe un archivo con las líneas dadas (cada una con '\n')
    f = open(path, "w")        # Abre en escritura (borra contenido anterior)
    i = 0
    while i < len(lines):      # Recorre lista
        f.write(lines[i] + "\n")  # Escribe línea + salto
        i = i + 1
    f.close()                  # Cierra archivo


def append_line(path, line):   # Añade una línea al final del archivo
    f = open(path, "a")        # Abre en append
    f.write(line + "\n")       # Escribe línea + salto
    f.close()                  # Cierra


def sort_by_ts(lines):         # Ordena la lista de líneas por timestamp (campo ts)
    def keyfun(x):             # Función clave: extrae ts desde el record
        ok, o, d, ts, st, tsst, msg = parse_record(x)  # Parsea la línea
        if ok:
            return ts          # Devuelve ts si parseó bien
        return "00000000000000"  # Si está mal formada, la manda al inicio (ts mínimo)
    lines.sort(key=keyfun)     # Ordena in-place por esa clave


def merge_record(path, record_line):  # Inserta o actualiza un registro dentro del archivo conversación
    # Inserta/actualiza por (origen,destino,ts,mensaje) y ordena cronológico
    okn, no, nd, nts, nst, ntsst, nm = parse_record(record_line)  # Parsea el nuevo record
    if not okn:              # Si el record nuevo es inválido
        return               # No hace nada

    lines = read_lines(path) # Lee conversación existente
    out = []                 # Lista de salida (actualizada)
    updated = False          # Bandera: si se actualizó un record existente

    i = 0
    while i < len(lines):    # Recorre cada línea existente
        ok, o, d, ts, st, tsst, msg = parse_record(lines[i])  # Parsea línea actual
        if ok:               # Si es válida
            if o == no and d == nd and ts == nts and msg == nm:
                # Si coincide por (origen, destino, ts, mensaje), es “el mismo mensaje”
                out.append(no + ";" + nd + ";" + nts + ";" + nst + ";" + ntsst + ";" + nm)
                # Reemplaza por la versión nueva (nuevo estado y ts_estado)
                updated = True  # Marca que ya se actualizó
            else:
                out.append(lines[i])  # Si no coincide, deja igual
        else:
            out.append(lines[i])      # Si línea inválida, la conserva tal cual
        i = i + 1

    if not updated:          # Si no encontró ninguna coincidencia
        out.append(record_line)  # Inserta el record nuevo al final

    sort_by_ts(out)          # Ordena cronológicamente por ts
    write_lines(path, out)   # Guarda archivo actualizado


def last_timestamp(path):    # Devuelve el mayor timestamp (ts) encontrado en el archivo
    lines = read_lines(path) # Lee líneas
    mx = "00000000000000"    # Máximo inicial (ts mínimo)
    i = 0
    while i < len(lines):    # Recorre todo
        ok, o, d, ts, st, tsst, msg = parse_record(lines[i])  # Parsea
        if ok:
            if ts > mx:      # Compara strings AAAAMMDDHHMMSS (orden lexicográfico funciona)
                mx = ts      # Actualiza máximo
        i = i + 1
    return mx                # Retorna último ts


import os  # (Repetido) Vuelves a importar os; no hace falta, pero no rompe nada

def list_local_peers(user_dir, user):  # Obtiene peers a partir de nombres de archivos locales
    # Devuelve lista de peers a partir de archivos:
    #   user_peer.txt
    # Ignora:
    #   user_peer_tmp.txt y otros...
    peers = []                     # Lista resultado
    prefix = user + "_"            # Prefijo obligatorio en nombre del archivo
    suffix = ".txt"                # Sufijo obligatorio

    try:
        files = os.listdir(user_dir)  # Lista archivos dentro del directorio del usuario
    except Exception:
        files = []                    # Si falla, trabaja con lista vacía

    i = 0
    while i < len(files):          # Recorre nombres
        name = files[i]            # Nombre de archivo actual

        ok = True                  # Bandera para validar nombre del archivo
        if not name.startswith(prefix):  # Debe empezar por "user_"
            ok = False
        if ok and not name.endswith(suffix):  # Debe terminar en ".txt"
            ok = False
        if ok and name.endswith("_tmp.txt"):  # Pero NO debe ser "_tmp.txt"
            ok = False

        if ok:
            # extraer peer entre prefix y .txt
            peer = name[len(prefix):]     # Quita "user_"
            peer = peer[:-len(suffix)]    # Quita ".txt"

            # filtro básico
            valid = True
            if peer == "":                # No vacío
                valid = False
            if valid and peer == user:    # No puede ser él mismo
                valid = False
            if valid and peer == "?":     # No se acepta el placeholder "?"
                valid = False
            if valid and peer.startswith("."):  # Evita archivos ocultos tipo ".DS_Store"
                valid = False

            if valid:
                # evitar duplicados
                if peer not in peers:     # Evita repetidos
                    peers.append(peer)    # Agrega

        i = i + 1

    peers.sort()                  # Orden alfabético
    return peers                  # Devuelve lista


def mark_delivered_to_read(conv_path, peer, user, ts_state):  # Convierte ENTREGADO -> LEIDO y genera receipts
    # Cambia ENTREGADO => LEIDO para mensajes peer -> user
    # Devuelve lista de líneas LEIDO para enviar al server por puerto ENVÍO
    lines = read_lines(conv_path)  # Lee conversación
    out = []                       # Líneas actualizadas
    receipts = []                  # Recibos LEIDO a enviar al servidor

    i = 0
    while i < len(lines):          # Recorre todas las líneas
        ok, o, d, ts, st, tsst, msg = parse_record(lines[i])  # Parsea
        if ok:
            if o == ("@" + peer) and d == ("@" + user) and st == "ENTREGADO":
                # Si es un mensaje entrante (peer -> user) y está ENTREGADO
                new_line = o + ";" + d + ";" + ts + ";LEIDO;" + ts_state + ";" + msg
                # Construye nueva línea marcándola como LEIDO con ts_state
                out.append(new_line)      # Guarda versión actualizada en conversación local
                receipts.append(new_line) # Guarda el receipt para mandarlo al servidor
            else:
                out.append(lines[i])      # Si no aplica, deja igual
        else:
            out.append(lines[i])          # Si línea inválida, la conserva
        i = i + 1

    write_lines(conv_path, out)           # Sobrescribe conversación con cambios
    return receipts                       # Devuelve lista de receipts (LEIDO) a enviar
