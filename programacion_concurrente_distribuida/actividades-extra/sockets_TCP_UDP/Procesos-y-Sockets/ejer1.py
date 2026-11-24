import os
import time
import multiprocessing
from random import randint

def corredor(nombre, archivo, distancia_total, lock):
    """
    Función que simula a un corredor avanzando en la carrera.
    Lee y actualiza el archivo correspondiente con la distancia recorrida.
    """
    leyendo = False
    while not leyendo:
        # Verifica si el archivo está marcado como "LEIDO"
        leyendo = True
        encontrado_leido = False
        while not encontrado_leido:
            if not os.path.exists("ESCRIBIENDO_" + archivo):
                f = open(archivo, "r")
                contenido = f.read()
                f.close()
                if "LEIDO" in contenido:
                    encontrado_leido = True
            else:
                time.sleep(0.1)

        # Marca el archivo como "en escritura"
        f = open("ESCRIBIENDO_" + archivo, "w")
        f.write("")
        f.close()

        # Lee la distancia actual (si existe) y avanza
        distancia = 0
        f = open(archivo, "r")
        contenido = f.read()
        f.close()
        if contenido.strip() and "LEIDO" not in contenido:
            distancia = int(contenido.strip())

        # Borra el contenido del archivo y escribe el nuevo avance
        distancia += randint(15, 80)  # se puede aumentar el rango de avance para que los corredores lleguen más rápido
        f = open(archivo, "w")
        if distancia >= distancia_total:
            f.write(nombre + " ha cruzado la meta con " + str(distancia) + " metros! Felicitaciones!\n")
            f.close()
            os.remove("ESCRIBIENDO_" + archivo)
            print(nombre + " ha cruzado la meta con " + str(distancia) + " metros!")
            leyendo = False
        else:
            f.write(nombre + " ha avanzado " + str(distancia) + " metros.\n")
            f.close()

        # Elimina el marcador de "en escritura"
        if os.path.exists("ESCRIBIENDO_" + archivo):
            os.remove("ESCRIBIENDO_" + archivo)
        time.sleep(randint(1, 2))

def proceso_padre(archivos, lock):
    """
    Función que supervisa la carrera, revisa los archivos y muestra un mensaje cuando un corredor cruza la meta.
    """
    meta = False
    while not meta:
        for archivo in archivos:
            if os.path.exists("ESCRIBIENDO_" + archivo):
                # Si el archivo está siendo utilizado, espera y sigue con el siguiente
                time.sleep(0.1)
            else:
                # Marca el archivo como "en escritura"
                f = open("ESCRIBIENDO_" + archivo, "w")
                f.write("")
                f.close()

                # Lee el contenido del archivo
                f = open(archivo, "r")
                contenido = f.read()
                f.close()

                # Marca el archivo como "LEIDO"
                if contenido.strip() and "LEIDO" not in contenido:
                    f = open(archivo, "a")
                    f.write("\nLEIDO")
                    f.close()

                    if contenido.strip().isdigit() and int(contenido.strip()) >= 100:
                        meta = True
                        print("Meta alcanzada por un corredor en " + archivo + " con " + contenido.strip() + " metros!")

                # Elimina el marcador de "en escritura"
                if os.path.exists("ESCRIBIENDO_" + archivo):
                    os.remove("ESCRIBIENDO_" + archivo)
        time.sleep(0.1)

def main():
    """
    Función principal que configura los archivos y lanza los procesos de los corredores.
    """
    corredores = ["Corredor1", "Corredor2", "Corredor3", "Corredor4", "Corredor5"]
    archivos = ["avance_" + str(i) + ".txt" for i in range(len(corredores))]
    distancia_total = 100

    # Inicializa los archivos con distancia 0 y el marcador LEIDO
    for archivo in archivos:
        f = open(archivo, "w")
        f.write("0\nLEIDO\n")
        f.close()

    # Verifica que los archivos se hayan generado correctamente
    print("Archivos generados correctamente: ", archivos)

    # Crea un lock para la sincronización
    lock = multiprocessing.Lock()

    # Crea los procesos de los corredores
    procesos = []
    for i in range(len(corredores)):
        p = multiprocessing.Process(target=corredor, args=(corredores[i], archivos[i], distancia_total, lock))
        procesos.append(p)
        p.start()

    # Proceso padre supervisa la carrera
    proceso_padre(archivos, lock)

    # Espera a que terminen los procesos de los corredores
    for p in procesos:
        p.join()

    # Limpia los archivos temporales
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)

if __name__ == "__main__":
    main()
