
import time
import threading

SLEEP = 5

def esperar(sec):
    print(f"Esperando {sec} segundos...")
    time.sleep(sec)
    print(f"... ya hemos despertado")

start = time.time()
previo = start
for x in range(2):
    esperar(SLEEP)
    end = time.time()
    print(f"la llamada {x+1} ha tardado {end - start} segundos")
    previo = end


end = time.time()

print(f"hemos tardado en total {end - start} segundos")