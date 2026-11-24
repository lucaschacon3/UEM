import threading

suma = 0
numeros= 100
def suma_hilos():
    global suma
    for i in range(1,101):
        suma += i
    print("el resultado final es => " ,suma)


t = threading.Thread(target=suma_hilos)

print("se ejecuta al inicio")
t.start()
t.join()
print("Hilo finalizado correctamente")
