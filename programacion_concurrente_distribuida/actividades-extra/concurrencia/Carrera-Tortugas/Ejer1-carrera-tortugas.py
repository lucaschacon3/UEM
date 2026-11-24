
import random
import time     #es una función útil para controlar el ritmo de la ejecución de tu programa, haciéndolo más pausado y fácil de seguir
import threading


# aleatorio para gener X tortugas
# aleatorio para generar Y velocidad y un Z distancia

# muestra los metros de recorrido de cada totuga
# el movimiento aleatorio terminara hasta q se llegue o supere la Z de 100 metros , distancia de met

# se muestra la tortuga que ganado o llegado a la meta

# el programa esperara a q todos los hilos osea procesos terminen antes de cerrarse o terminar 




# Clase TORTUGA
class Tortuga:
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.velocidad = 0 #La velocidad se asigna aleatoriamente más adelante
        self.distancia = 0 #La tortuga comienza en el punto 0 (sin avanzar)

    # Método para mover la tortuga: genera una nueva velocidad y actualiza la distancia recorrida
    def mover(self):
        self.velocidad = random.randint(1, 10) #Generar una velocidad aleatoria entre 1 y 10 en cada movimiento
        self.distancia += self.velocidad #Aumentar la distancia según la velocidad

    # Método que retorna una representación en texto del estado de la tortuga
    def __str__(self):
        return f"{self.nombre}: ha recorrido {self.distancia} metros (Velocidad: {self.velocidad})"


# Función que maneja la carrera entre las tortugas
def mover_tortugas(cantidad_tortugas):
    tortugas = [] #lista vacía donde se almacenarán todas las tortugas participantes

    # Crear y agregar tortugas a la lista
    for i in range(cantidad_tortugas):
        nombre_tortuga = f"Tortuga {i + 1}"  #asignacion de nombres únicos como "Tortuga 1", "Tortuga 2", etc.

        tortuga = Tortuga(nombre_tortuga) #se crea una instancia de la clase tortuga 
        tortugas.append(tortuga)          #y se agrega a la lista de tortugas

    #hay_ganadora = False    #variable booleana que controlará si ya hay una ganadora
    tortuga_ganadora = None #variable que almacenará la tortuga ganadora
    todas_en_meta = False   #variable que controlará si todas las tortugas llegaron a la meta

    # Mientras no haya una tortuga que haya cruzado la meta, se siguen moviendon
    while not todas_en_meta:
        todas_en_meta = True  #se supone q todas llegaron, en caso q no se cambia a False
        for tortuga in tortugas: 
            if tortuga.distancia < 100:  #si la tortuga aún no llega a la meta
                tortuga.mover() #Mover la tortuga, actualizadno su velocidad y distancia 
                #print(tortuga)  #Imprimir el estado actual de la tortuga
                todas_en_meta = False  #si alguna tortuga sigue corriendo, se cambia a False

            # Verificar si alguna tortuga ha llegado a la meta
            if tortuga.distancia >= 100 and not tortuga_ganadora:
                tortuga_ganadora = tortuga #la primera que llegue será marcada como ganadora
                #hay_ganadora = True  #se cambia el valor de la booleana si hay ganadora

        dibujar_carrera(tortugas)  #bibuja el estado actual de la carrera
        time.sleep(0.3)            #pausa para simular el tiempo de movimiento de las tortugas
        print("-----")             #separador visual para cada turno

    # Anunciar la tortuga ganadora
    print(f"¡{tortuga_ganadora.nombre} ha ganado la carrera al recorrer primera {tortuga_ganadora.distancia:.2f} metros!")
    print("¡Todas las tortugas han llegado a la meta!")


# Función para dibujar la pista y las tortugas en cada turno
def dibujar_carrera(tortugas, longitud_pista=50):
    print("\n" * 50)  #"limpia" la pantalla 
    meta = longitud_pista
    
    # Dibuja cada tortuga en la pista
    for tortuga in tortugas:
        avance = int((tortuga.distancia / 100) * longitud_pista)  #escala la distancia a la longitud de la pista
        pista = '-' * avance + '🐢' + '-' * (meta - avance)
        print(f"{tortuga.nombre}: {pista} {tortuga.distancia:.2f}m")

    print("\n" + "+" + "-"*longitud_pista + "+ META")  # Línea de meta


# Función para mostrar la cuenta regresiva antes de comenzar la carrera
def cuenta_regresiva():
    print("\n--------------------------------------------")
    print("¡BIENVENIDOS A LA GRAN CARRERA DE TORTUGAS!")
    print("--------------------------------------------\n")
    print("LA CARRERA COMENZARÁ EN:")
    for i in range(3, 0, -1):  # Cuenta regresiva de 3 a 1
        print(f"{i}...")
        time.sleep(1.5)  # Pausa de 1 segundo entre cada número 
    print("¡A correr!\n")
    time.sleep(0.5)  # Pausa adicional antes de comenzar la carrera




# Main :  Punto de inicio del programa
if __name__ == "__main__":

    # Mostrar cuenta regresiva
    #cuenta_regresiva()
    # Con Hilos
    hilo1 = threading.Thread(target=cuenta_regresiva)

    # Determinar aleatoriamente la cantidad de tortugas en la carrera
    # cantidad_tortugas = random.randint(3, 6)  #se puede cambiar el número de tortugas aleatorias , en este caso entre 3 y 6 
    print("Ingrese la cantidad de las tortugas: ")
    cantidad_tortugas 
    #print(f"Cantidad de tortugas en la carrera: {cantidad_tortugas}")
    print("Cantidad de tortugas en la carrera: " , cantidad_tortugas)
    print("\nLa carrera comienza ahora...\n")

    # Iniciar la carrera de las tortugas
    #mover_tortugas(cantidad_tortugas) #funcion q maneja la carrera con la cantidad de tortugas generadas
    # Con Hilos
    hilos2 = threading.Thread(target=mover_tortugas(cantidad_tortugas))

