import threading
from time import sleep
from random import randint
import queue

def iniciar(nEjecutadores):
    hilos = []
    for i in range(nEjecutadores):
        hilos.append(threading.Thread(target = ejecutar_tarea, name = "Ejecutador " + str(i+1)))
    hilos.append(threading.Thread(target = usuario, args=(numTareas,), name = "Usuario"))

    for x in hilos:
        x.start()

    for x in hilos:
        x.join()


def usuario(nTareas):
    global tareas
    for i in range(nTareas):
        agregar_tarea(tareas[i][0], tareas[i][1])
        sleep(randint(1,2))
    if mutexConsola.acquire():
        print("Se han agregado todas las tareas a ejecutar en la cola")
        mutexConsola.release()

def agregar_tarea(nombre, duracion):
    global tareasCola
    tareaAgregada = False
    while not tareaAgregada:
        if mutexCola.acquire():
            tareasCola.put((duracion, nombre))
            mutexCola.release()
            tareaAgregada = True
            if mutexConsola.acquire():
                print(f"Se agrego la tarea {nombre} con duracion {duracion}")
                mostrar_tareas_pendientes()
                mutexConsola.release()

def ejecutar_tarea():
    global numTareas, tareasCola, tareasCompletadas
    while len(tareasCompletadas) != numTareas:
        if mutexCola.acquire(timeout=2):
            if not tareasCola.empty():
                duracion, nombre = tareasCola.get()
                mutexCola.release()
                if mutexConsola.acquire():
                    print(threading.current_thread().name + f", ejecutando la tarea {nombre} con duracion {duracion}")
                    mutexConsola.release()
                    sleep(duracion/1000)
                    if mutexConsola.acquire():
                        print(threading.current_thread().name + f", tarea {nombre} terminada.")
                        tareasCompletadas.append((nombre, duracion))
                        mostrar_tareas_completadas()
                        mutexConsola.release()
            else:
                mutexCola.release()

def mostrar_tareas_pendientes(): 
    print("Tareas pendientes:")
    print(tareasCola.queue)

def mostrar_tareas_completadas(): 
    print("Tareas completadas:")
    print(tareasCompletadas)

tareas = [
    ["Microsoft Word", randint(1, 60)],
    ["Excel", randint(1, 60)],
    ["PowerPoint", randint(1, 60)],
    ["Adobe Photoshop", randint(1, 60)],
    ["Adobe Illustrator", randint(1, 60)],
    ["Google Chrome", randint(1, 60)],
    ["Mozilla Firefox", randint(1, 60)],
    ["Slack", randint(1, 60)],
    ["Zoom", randint(1, 60)],
    ["Spotify", randint(1, 60)],
    ["Notepad++", randint(1, 60)],
    ["Visual Studio Code", randint(1, 60)],
    ["Eclipse", randint(1, 60)],
    ["Sublime Text", randint(1, 60)],
    ["GitHub Desktop", randint(1, 60)],
    ["Microsoft Outlook", randint(1, 60)],
    ["Trello", randint(1, 60)],
    ["Asana", randint(1, 60)],
    ["Dropbox", randint(1, 60)],
    ["OneDrive", randint(1, 60)],
    ["Evernote", randint(1, 60)],
    ["Quip", randint(1, 60)],
    ["Skype", randint(1, 60)],
    ["TeamViewer", randint(1, 60)],
    ["Remote Desktop", randint(1, 60)],
    ["VirtualBox", randint(1, 60)],
    ["VMware Workstation", randint(1, 60)],
    ["MATLAB", randint(1, 60)],
    ["RStudio", randint(1, 60)],
    ["SAS", randint(1, 60)],
    ["SPSS", randint(1, 60)],
    ["Tableau", randint(1, 60)],
    ["Microsoft Access", randint(1, 60)],
    ["QuickBooks", randint(1, 60)],
    ["TurboTax", randint(1, 60)],
    ["Salesforce", randint(1, 60)],
    ["Mailchimp", randint(1, 60)],
    ["Hootsuite", randint(1, 60)],
    ["Canva", randint(1, 60)],
    ["Figma", randint(1, 60)],
    ["InVision", randint(1, 60)],
    ["AutoCAD", randint(1, 60)],
    ["Sketch", randint(1, 60)],
    ["SolidWorks", randint(1, 60)],
    ["Unity", randint(1, 60)],
    ["Unreal Engine", randint(1, 60)],
    ["Blender", randint(1, 60)],
    ["Adobe Premiere Pro", randint(1, 60)],
    ["Final Cut Pro", randint(1, 60)],
    ["iMovie", randint(1, 60)],
    ["Windows Media Player", randint(1, 60)],
    ["VLC Media Player", randint(1, 60)],
    ["Avid Media Composer", randint(1, 60)],
    ["CamStudio", randint(1, 60)],
    ["OBS Studio", randint(1, 60)],
    ["Norton Antivirus", randint(1, 60)],
    ["Malwarebytes", randint(1, 60)],
    ["CCleaner", randint(1, 60)],
    ["AnyDesk", randint(1, 60)],
    ["Spotify", randint(1, 60)],
    ["Apple Music", randint(1, 60)],
    ["Google Play Music", randint(1, 60)],
    ["Pandora", randint(1, 60)],
    ["Pocket Casts", randint(1, 60)],
    ["Audacity", randint(1, 60)],
    ["GarageBand", randint(1, 60)],
    ["Pro Tools", randint(1, 60)],
    ["Ableton Live", randint(1, 60)],
    ["FL Studio", randint(1, 60)],
    ["Sibelius", randint(1, 60)],
    ["Notion", randint(1, 60)],
    ["Microsoft Project", randint(1, 60)],
    ["Jira", randint(1, 60)],
    ["Confluence", randint(1, 60)],
    ["Miro", randint(1, 60)],
    ["Lucidchart", randint(1, 60)],
    ["MindMeister", randint(1, 60)],
    ["XMind", randint(1, 60)],
    ["SketchUp", randint(1, 60)],
    ["Tinkercad", randint(1, 60)],
    ["Fusion 360", randint(1, 60)],
    ["Paint.NET", randint(1, 60)],
    ["GIMP", randint(1, 60)],
    ["CorelDRAW", randint(1, 60)],
    ["Cinema 4D", randint(1, 60)],
    ["Houdini", randint(1, 60)],
    ["ZBrush", randint(1, 60)],
    ["Rhinoceros", randint(1, 60)],
    ["Postman", randint(1, 60)],
    ["Insomnia", randint(1, 60)],
    ["Swagger", randint(1, 60)],
    ["FileZilla", randint(1, 60)],
    ["Cyberduck", randint(1, 60)],
    ["WinRAR", randint(1, 60)],
    ["7-Zip", randint(1, 60)],
    ["VirtualBox", randint(1, 60)],
    ["Kdenlive", randint(1, 60)],
    ["Discord", randint(1, 60)],
    ["Crunchyroll", randint(1, 60)],
    ["Steam", randint(1, 60)],
]

tareasCola = queue.PriorityQueue()
tareasCompletadas = []
mutexCola = threading.Lock()
mutexConsola = threading.Lock()
nEjecutadores = int(input("Introduce el maximo numero de tareas que quieres poder ejecutar a la vez: "))
numTareas = int(input("Introduce el numero de tareas a ejecutar(max 100): "))
iniciar(nEjecutadores)
print("Terminamos la simulacion del administrador de tareas")

# #5. Desarrolla un administrador de tareas para un sistema operativo. Los procesos (tareas) se ejecutan de manera
# concurrente, y el administrador debe coordinar la ejecución de las tareas. Utiliza una cola (queue) para gestionar la
# ejecución de las tareas.

# En este ejercicio, debes implementar las siguientes funciones:

# agregar_tarea(nombre, duracion): Esta función agrega una nueva tarea a la cola de tareas pendientes. Debes
# especificar el nombre de la tarea y su duración estimada en segundos.

# ejecutar_tarea(): Esta función toma la tarea de mayor prioridad (aquella con la duración más corta) de la cola de
# tareas pendientes y la ejecuta. Debes simular la ejecución de la tarea mediante un retraso de la duración especificada.

# mostrar_tareas_pendientes(): Esta función muestra la lista de tareas pendientes en la cola.

# mostrar_tareas_completadas(): Esta función muestra la lista de tareas que han sido ejecutadas.

# Utiliza una cola para gestionar las tareas pendientes y asegurarte de que las tareas se ejecuten en el orden correcto:
# es decir: primero las tareas más cortas.