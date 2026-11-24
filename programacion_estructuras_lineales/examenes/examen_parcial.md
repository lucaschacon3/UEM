# Examen: Programación con estructuras lineales

**Universidad Europea**  
*Departamento de Ciencia, Computación y Tecnología — Escuela STEAM*

---

- **Nombre:** 
- **Apellidos:** 
- **Nº Expediente:** 
- **Fecha:** 
- **Vidas disponibles:** ❤️ ❤️ ❤️
- **Calificación:** 

---

## Normas del examen

- **Duración del Examen:** El examen tiene una duración de 1 hora y 30 minutos.
- **Estructura del Examen:**
  - El 30% de la calificación del examen consistirá en preguntas de tipo test con justificación.
  - El 70% de la calificación del examen consistirá en preguntas de desarrollo.
- **Material Permitido:**
  - NO se permite el uso de libros, apuntes, dispositivos electrónicos ni cualquier otro material de consulta durante el examen.
  - Esto incluye teléfonos móviles, auriculares de cualquier tipo, relojes inteligentes, etc.
  - NO se permite el uso de **lapiceros** o bolígrafo de color **ROJO**.
- **Comportamiento:**
  - Mantén silencio durante todo el examen.
  - No se permite la comunicación entre estudiantes.
  - Levanta la mano si necesitas asistencia del profesor.
  - Cada estudiante tendrá 3 "vidas" (preguntas) que podrá hacer durante el examen.
- **Entrega del Examen:**
  - Asegúrate de escribir tu nombre y número de estudiante en todas las hojas del examen.
  - Entrega todas las hojas al finalizar el examen, incluso las que no hayas utilizado.
  - Cuando queden 10 minutos para finalizar el examen, se anunciará el tiempo restante.
  - Debes detener la escritura inmediatamente cuando se indique el final del tiempo.
- **Integridad Académica:** Cualquier intento de copiar resultará en la anulación del examen. Si se incumple alguna de estas normas, el resultado será el mismo. Pudiendo conllevar sanciones más allá de la propia evaluación.
- **Puntuación del examen:** Este examen cuenta con un ejercicio "extra" de 0.5 puntos. Estos puntos **no cuentan para el aprobado**, es decir, debe obtenerse una calificación de 5 o más para poder rascar ese medio punto extra.

---

## Sección 1

Responde las preguntas tipo test. De ninguna manera se restarán puntos con las respuestas incorrectas. Pero debes justificar de alguna forma porqué has elegido la opción marcada. En caso de no responder alguna de las opciones con una justificación, no se contabilizará para el total de puntos del examen.

**Pregunta 1:** ¿Cuál de las siguientes afirmaciones define correctamente un Tipo Abstracto de Datos?
- a) Es una clase que almacena todos sus atributos como miembros públicos.
- b) Es una organización concreta de datos que utiliza necesariamente memoria dinámica.
- c) Es un conjunto de variables que carece de operaciones asociadas.
- d) Es un modelo que define valores y operaciones a partir de su comportamiento, sin imponer una representación interna concreta.

**Pregunta 2:** Teniendo en cuenta las operaciones disponibles en una pila... ¿Qué pareja está formada exclusivamente por operaciones consultoras?
- a) `apilar()` y `desapilar()`
- b) `vacía()` y `apilar()`
- c) `tamaño()` y `vacía()`
- d) `cima()` y `desapilar()`

**Pregunta 3:** Una pila de capacidad `N` utiliza un array `elementos` y una variable `cantidad`, que indica cuántos elementos contiene. Los elementos válidos ocupan posiciones consecutivas desde el índice cero. Si la pila no está vacía, ¿qué expresión permite acceder a su cima?
- a) `elementos[cantidad]`
- b) `elementos[0]`
- c) `elementos[N]`, independientemente del número de elementos.
- d) `elementos[cantidad - 1]`

**Pregunta 4:** ¿Qué sucede al finalizar el siguiente bloque, suponiendo que la reserva de memoria se realiza correctamente?

```cpp
{
    int* dato = new int(25);
}
```

- a) El entero se destruye automáticamente porque el puntero tiene ámbito local.
- b) La variable `dato` deja de existir, pero el entero reservado permanece sin liberar y se produce una fuga de memoria.
- c) Tanto el puntero como el entero permanecen accesibles desde cualquier función.
- d) El compilador inserta automáticamente una llamada a `delete`.

**Pregunta 5:** Una operación garantiza que, si se produce una excepción, el objeto conserva exactamente el estado que tenía antes de iniciar la operación. ¿Qué garantía ofrece?
- a) Garantía fuerte.
- b) Garantía básica.
- c) Garantía de no lanzamiento.
- d) Ninguna garantía, porque una operación segura no puede lanzar excepciones.

**Pregunta 6:** ¿Cuál de las siguientes situaciones aplica correctamente el principio RAII?
- a) Reservar memoria con `new` y confiar en que el sistema operativo la libere cuando termine el programa.
- b) Utilizar un puntero local y asumir que el recurso se libera cuando el puntero sale de ámbito.
- c) Encapsular un recurso en un objeto que lo adquiere durante su construcción y lo libera en su destructor.
- d) Sustituir las llamadas a `delete` por asignaciones de `nullptr` a los punteros propietarios.

---

## Sección 2

**Ejercicio 1:** Diseña un diagrama de clases para un videojuego. Cada personaje tiene un *nombre*, *puntos de vida* y una *[...]* objetos almacenados *en el inventario*. Al personaje se le deben poder consultar los puntos de vida, debe *[recibir]* daño y se deben poder añadir elementos al inventario. Incluye los atributos y métodos necesarios, sus tipos *[...]* (1 punto). **NO es necesario ESCRIBIR CODIGO.**

**Ejercicio 2:** Especifica una jerarquía de clases para los siguientes tipos de datos: `Router`, `DispositivoDeEntrada`, `Narvelizae`, `OrdenadorDeSobremesa`, `Monitor`, `Periferico`, `Raton`, `DispositivoDeRed`, `VisorVR`, `Pantalla`, `Hub`, `Dispositivo`, `Teclado`, `DispositivoDeSalida`, `Ordenador`. (1 punto) Justifica el porqué de dicha jerarquía.

**Ejercicio 2.5:** Detalla y especifica qué es un Narvelizae (0.5 puntos extras).

**Ejercicio 3:** ¿Qué significa pasar un objeto por referencia? ¿Qué implica su manejo? (1 punto)

**Ejercicio 4:** Dado el siguiente código, representa el diagrama de memoria (1 punto). Representa el estado por fases de la pila de ejecución del programa (1 punto).

```cpp
void modificar(int* valor, int* datos) {
    int incremento = 5;
    *valor += incremento;
    datos[1] = *valor;
}

int sumar(const int* datos) {
    int resultado = datos[0] + datos[1] + datos[2];
    return resultado;
}

int main() {
    int numero = 10;
    int* p = &numero;
    int* datos = nullptr;
    datos = new int[3]{10, 4, 9};

    modificar(p, datos);
    int total = sumar(datos);

    delete[] datos;
    datos = nullptr;
    p = nullptr;

    return 0;
}
```

**Ejercicio 5:** Representa y explica los diferentes espacios de memoria virtual de un programa (1 punto).

**Ejercicio 6:** Considerando la clase `"Registro"`, responde de forma justificada las siguientes cuestiones:
- a) Representa la distribución del objeto en memoria. Determina su tamaño total y la alineación del objeto (0,4 puntos).
- b) ¿Es posible optimizar el objeto para reducir su tamaño? En caso de ser posible, representa la nueva distribución e indica su tamaño total (0,4 puntos).
- c) Calcula el tamaño de una lista de 100 objetos del tipo Registro antes y después de la optimización, indicando cuánta memoria se ahorraría (0,2 puntos).

```cpp
class Registro {
private:
    char tipo;
    float medida;
    bool* activo;
    int identificador;
    char categoria;
    // ...
};
```