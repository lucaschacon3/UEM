"""ACTIVIDAD 1 - BARRERA 
Cada Alumno repsetn un hilo
El Aula representa la Barrera    
"""

import threading
import time
import random

#Barrera (aula) para sincronizar 5 hilos (estudiantes)
aula = threading.Barrier(5)

#Lock para sincronizar el mensaje de inicio del examen
inicio_examen_lock = threading.Lock()
examen_iniciado = False # pylint: disable=invalid-name

#Función que representará la llegada de cada estudiante
def asistencia(id_alumno):
    """Función que simula la asistencia de cada alumno al aula"""

    print("Alumno", id_alumno + 1, " estoy en camino") #mensaje q indica que el alumn está en camino
    tiempo_de_llegada = random.randint(1,5) #tiempo aleatorio de llegada
    time.sleep(tiempo_de_llegada) #simula el tiempo de llegada usando una pausa

    print("Alumno", id_alumno + 1, " he llegado al aula en " , tiempo_de_llegada , " horas")
    aula.wait() #el alumno espera hasta q todos hayan llegado

    #Lock para que el mensaje se imprime solo una vez
    global examen_iniciado #global para poder modificar su valor
    with inicio_examen_lock:   #para q solo un hilo a la vez puede ejecutarlo y no haya duplicados
        if not examen_iniciado: #se verifica si el mensaje aún no ha sido impreso
            print("\n--------------------------------\n"
                +" Estudiantes empezando el Exámen"
                +"\n--------------------------------")
            examen_iniciado = True    #se marca como true para evitar repeticion

    print("Alumno", id_alumno + 1, " empieza el examen y continua su camino")


#Lista para almacenar los hilos que representarán a cada estudiante
estudiantes = []

#Se crea y agrega 5 hilos(alumnos) a la lista
for i in range (5):
    #se crea un hilo, pasandole la función y el id del alumno
    alumno = threading.Thread(target=asistencia, args=(i,))
    estudiantes.append(alumno) #se agrega el hilo (alumno) a la lista de estudiantes

print("\n--------------------------------\n"
    + " Estudiantes saliendo de Casa"
    + "\n--------------------------------")

#Se inicia cada hilo para que cada alumno empiece su camino hacia el aula
for alumno in estudiantes:
    alumno.start()

print("\n----------------------------------\n"
    + " Estudiantes llegando a Clase"
    + "\n----------------------------------")

#Se espera a q todos los hilos(alumnos) completen su ejecución antes de continuar
for alumno in estudiantes:
    alumno.join()


# print("\nEstudiantes empezando el Exámen")

# El join es hasta q finalizacin los prcesos, pero la barrear se puede poner en intermedio
# no necesariemante al final
