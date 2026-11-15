
El programa se basa en los siguientes componentes:

- **Constante de distancia (`DISTANCIA_META`):** Los 100 metros que definen las distancia del recorrido y el final de la ejecución de cada hilo.
- **Lista con la clasificación (`clasificion`):** Es una lista global donde cada hilo almacena una tupla `(nombre, tiempo_total)` al completar su recorrido.
- **Función concurrente (`mover_tortuga`):**
    - Registra el inicio de la carrera con `time.time()`.
    - Bucle `while` mientras el progreso sea inferior a 100 metros (la meta).
    - Genera en cada iteración un avance aleatorio entre 1 y 20 metros (`random.randint(1, 20)`) y una pausa entre 1 y 2 segundos (`time.sleep(random.randint(1, 2))`), permitiendo el intercalado entre hilos.
    - Al alcanzar o superar los 100 metros, calcula la duración total y mete el resultado en la tupla de clasificación.
    
    !image.png
    
- **Gestión de hilos:**
    - Se instancian e inician 3 hilos (`Tortuga-0`, `Tortuga-1`, `Tortuga-2`).
    - Mediante un segundo bucle con `hilo.join()`, el hilo principal espera que terminen todos los hilos.
    
    !image.png
    
- **El ganador:** Cuando acaban los hilos, ordenamos la lista y en la primera posición estará la tupla con el nombre y el tiempo del ganador.

!image.png

---

**Ejecución:** 

Cada vez que se ha ejecutado el resultado ha sido distinto, se puede ver en la ejecución como los hilos se van intercalando sin seguir un orden:

!image.png

---

**Conclusiones**

Este ejercicio sirve para darse cuenta de como cuando un hilo está a la espera se puede ejecutar otro, mejorando la rapidez de ejecución.