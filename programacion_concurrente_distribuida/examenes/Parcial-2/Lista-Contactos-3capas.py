import threading
import time
import random


############# CAPA DE PRESENTACION #############
#                                                                                                      #   
#

def mostrarMenu(listaOpciones):
    opcionesElegidas = 0
    respuesta = " "
    for x in range(len(listaOpciones) ):
        print(f"{x + 1}. {listaOpciones[x] }")
    respuesta =input("Opcion: ")
    match(respuesta):
        case "1":
            opcionesElegidas = 0
        case "2":
            opcionesElegidas = 1
        case "3":
            opcionesElegidas = 2
        case "4":
            opcionesElegidas = 3
        case "5":
            opcionesElegidas = 4
        case _:
            print("Opcion no valida")

    return opcionesElegidas

def menu():
    opciones = []
    opciones.append("VER CONTACTOS")    
    opciones.append("AGREGAR CONTACTO")
    opciones.append("ELIMINAR CONTACTO")
    opciones.append("MODIFICAR CONTACTO")      
    opciones.append("SALIR")      
    mostrarMenu(opciones)




