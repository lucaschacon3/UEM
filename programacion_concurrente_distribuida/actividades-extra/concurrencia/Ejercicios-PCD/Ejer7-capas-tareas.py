

tareas = []


#capa de acceso de datos

def datos_agregar_tarea(nueva_tarea):
    global tareas
    tareas.append(nueva_tarea)

def datos_eliminar_tarea_de_lista(posicion):
    global tareas
    if (posicion >= 0) and (posicion < len(tareas)):
        tarea = tareas.pop(posicion)
        return tarea
    else:
        return tarea



#capa de logica de negocio

def negocio_agregar_tarea(nueva_tarea):
    datos_agregar_tarea(nueva_tarea)

def negocio_eliminar_tarea(tareas, tarea_a_borrar):
    pos_t = 0
    eliminada = ""
    for t in tareas:
        if t == tarea_a_borrar:
            eliminada = datos_eliminar_tarea_de_lista(pos_t)
        pos_t += 1

def negocio_mostrar_tareas(tareas):
    listado_mostrar = ""
    i = 0
    for t in tareas:
        cabecera = i + " ->"
        listado_mostrar += cabecera + " La Tarea " + t + " esta en la lista"
        listado_mostrar += "\n"
    return listado_mostrar



#capa de presentacion / usuario

def presentacion_agregar_tarea(tarea):
    negocio_agregar_tarea(tarea)
    print("La Tarea ha sido agregada")

def crear_tarea():
    print("Dime el nombre de la tarea que quiere crear")
    tarea_nueva = input()
    presentacion_agregar_tarea(tarea_nueva)