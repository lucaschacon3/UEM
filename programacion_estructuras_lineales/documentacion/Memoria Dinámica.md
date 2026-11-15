# Memoria Dinámica en C++ (Sesión 2)

**Asignatura:** Programación con Estructuras Lineales  
**Unidad:** Memoria Dinámica

---

## Objetivos de la sesión

* **Puntero nulo:** Distinguir un puntero sin inicializar de `nullptr`.
* **Reservar memoria:** Usar `new` y `new[]` comprendiendo sus dos fases (reservar y construir).
* **Liberar memoria:** Usar `delete` y `delete[]` correctamente y siempre emparejados.
* **Fugas de memoria:** Reconocer un *memory leak* y el uso de punteros tras liberar memoria (*dangling pointers*).
* **Fragmentación:** Explicar por qué puede existir memoria libre que no se puede utilizar.
* **Aritmética de punteros:** Relacionar `p + i`, `*(p + i)` y `p[i]`.

---

## 0. Repaso: Punteros, Stack y Free Store

### Dirección, puntero y desreferencia

```cpp
int n = 10;
int* p = &n;
*p = 20;
```

* **`p`**: almacena la **dirección de memoria** de `n` (por ejemplo, `0x7ffe10`).
* **`*p`**: representa el **objeto que vive en esa dirección** (la propia variable `n`).
* Tras ejecutar `*p = 20;`, el valor de `n` pasa a ser `20`.

### Stack vs. Free Store

| Característica | Stack (Pila) | Free Store (Memoria libre / Heap) |
| :--- | :--- | :--- |
| **Qué almacena** | Variables locales y marcos de llamadas a funciones. | Objetos y arrays dinámicos creados con `new` / `new[]`. |
| **Orden / Organización** | Crece y decrece en orden LIFO (*Last In, First Out*). | Bloques asignados y liberados en cualquier orden. |
| **Gestión de vida** | Automática (al salir del ámbito, desaparece). | Controlada explícitamente por el programador (`new` / `delete`). |
| **Tamaño** | Limitado ($\approx 1\text{--}8\text{ MB}$). | Grande, con tamaño decidido en tiempo de ejecución. |

### ¿Por qué necesitamos memoria dinámica?

1. **Problema 1 — Tiempo de vida:** Cuando una función termina, su marco de pila desaparece y con él todas sus variables locales. La memoria dinámica permite que un objeto siga existiendo más allá del ámbito donde se creó.
2. **Problema 2 — Tamaño desconocido:** A menudo no sabemos cuántos elementos necesitaremos hasta que el programa está en ejecución (por ejemplo, cuando el usuario introduce la cantidad por teclado).

---

## 1. El puntero nulo: `nullptr`

### El problema: punteros sin inicializar

```cpp
int* p;            // ¿A qué apunta? Valor indeterminado
std::cout << *p;   // INCORRECTO: Comportamiento indefinido (UB)
```

Un puntero sin inicializar contiene una secuencia arbitraria de bits (basura). Desreferenciarlo provoca **comportamiento indefinido (*Undefined Behavior*)**: puede fallar inmediatamente, imprimir basura o parecer que funciona hoy y fallar mañana.

### La solución: `nullptr`

```cpp
int* p = nullptr;
```

* Significa explícitamente que `p` **no apunta actualmente a ningún objeto válido**.
* `nullptr` **no** significa que el puntero no exista: la variable `p` existe en memoria, pero su valor indica que no referencia nada.
* **Nota histórica:** En C y C++ antiguo se usaba `NULL` o `0`. Desde **C++11** se utiliza `nullptr`, que tiene su propio tipo (`std::nullptr_t`), siendo más seguro y claro.

### Comparación: sin inicializar vs. `nullptr`

| Aspecto | `int* p;` (Sin inicializar) | `int* p = nullptr;` (Puntero nulo) |
| :--- | :--- | :--- |
| **Valor** | Indeterminado. | Puntero nulo. |
| **Destino** | Desconocido. | Sabemos con certeza que no apunta a nada. |
| **Comprobación** | No se puede comprobar si es válido. | Se puede comprobar con `p != nullptr`. |
| **Seguridad** | Desreferenciarlo produce UB. | Explícito, legible y comprobable. |

### Comprobación antes de usar

Desreferenciar `nullptr` **también es comportamiento indefinido** (en la práctica suele provocar un fallo de segmentación o *segmentation fault*). Siempre se debe comprobar antes de desreferenciar:

```cpp
// Forma explícita (recomendada para mayor claridad)
if (p != nullptr) {
    std::cout << *p;
}

// Forma abreviada equivalente
if (p) {
    std::cout << *p;
}
```

### Usos típicos de `nullptr`
* Marcar el final de una lista enlazada o de un recorrido (no hay nodo siguiente).
* Indicar que "todavía no hay objeto" asignado.
* Señalar que una operación no ha tenido éxito (por ejemplo, buscar un elemento y no encontrarlo).
* Limpiar un puntero tras liberar su memoria con `delete`.

---

## 2. Memoria libre y la expresión `new`

### Variable local vs. Objeto dinámico

* `int n = 10;` $\rightarrow$ **Una sola entidad**: el objeto local `n` en el *stack*.
* `int* p = new int;` $\rightarrow$ **Dos entidades distintas**:
  1. El puntero `p` (variable local en el *stack*).
  2. Un `int` sin nombre (en la *free store*).

### Inicializar, leer y modificar

```cpp
int* p = new int{10};   // Crea un int con valor 10 en la free store y guarda su dirección en p
std::cout << *p;        // Accede al objeto apuntado: imprime 10
*p = 20;                // Modifica el objeto apuntado (NO modifica la dirección guardada en p)
```

### Tiempos de vida distintos

```cpp
{
    int* p = new int{10};
} // Fin del bloque: p desaparece (es local), pero el 10 en la free store sigue reservado
```

> **Idea clave:** Al salir del ámbito, el puntero local `p` se destruye automáticamente, pero el objeto creado con `new` **no se destruye**. Como nadie conserva ya su dirección, queda inaccesible (origen de las fugas de memoria).

### `new` con estructuras

```cpp
struct Student {
    std::string name;
    double grade1, grade2, grade3;
    double average() const { return (grade1 + grade2 + grade3) / 3.0; }
};

Student* p = new Student{"Ana", 7.0, 8.0, 9.0};

std::cout << p->name;       // Imprime: Ana   (equivale a (*p).name)
std::cout << p->average();  // Imprime: 8
```

### ¿Qué hace `new` por dentro?

Al ejecutar `X* p = new X{/* argumentos */};`, ocurren internamente estas fases:
1. **Reservar memoria:** Busca al menos `sizeof(X)` bytes contiguos y correctamente alineados en la memoria libre.
2. **Construir el objeto:** Ejecuta el constructor de `X` sobre esa memoria con los argumentos proporcionados. *(Si el constructor falla lanzando una excepción, la memoria reservada se libera automáticamente antes de propagar el error).*
3. **Devolver la dirección:** La expresión devuelve un puntero `X*` al objeto recién creado, que se almacena en `p`.

### `sizeof(T)` y fallo de reserva (`std::bad_alloc`)

El operador `sizeof(T)` devuelve cuántos bytes ocupa un tipo `T` (excepto `char`, que siempre es 1 byte, los tamaños dependen de la plataforma):
* `char`: 1 byte (siempre)
* `int`: 4 bytes (típico)
* `double`: 8 bytes (típico)
* `int*` (64 bits): 8 bytes (típico)

Si no hay memoria suficiente disponible, `new` lanza la excepción **`std::bad_alloc`** (definida en `<new>`):

```cpp
#include <new>
#include <iostream>

try {
    int* q = new int[n];
} catch (const std::bad_alloc& e) {
    std::cout << "Sin memoria\n";
}
```
* **Alternativa sin excepciones:** `int* q = new (std::nothrow) int[n];` devuelve `nullptr` si falla en lugar de lanzar una excepción.

### Arrays dinámicos: `new[]`

Permiten crear secuencias contiguas de elementos cuyo tamaño se decide en tiempo de ejecución:

```cpp
int* p1 = new int[5];       // 5 enteros consecutivos SIN inicializar (basura)
int* p2 = new int[5]{};     // 5 enteros consecutivos inicializados a 0
Student* p3 = new Student[100]; // 100 objetos Student creados con su constructor por defecto
```

#### Comparación: Array estático vs. Array dinámico

| Característica | `int datos[100];` | `int* datos = new int[n];` |
| :--- | :--- | :--- |
| **Tamaño** | Fijo, conocido al compilar. | Decidido en tiempo de ejecución. |
| **Dónde vive** | *Stack* (pila). | *Free store* (memoria libre). |
| **Liberación** | Automática al salir del ámbito. | Manual con `delete[] datos;`. |
| **Límite de tamaño** | Pila pequeña. | Memoria libre (grande). |

---

## 3. `delete`, `delete[]` y fugas de memoria

### Fugas de memoria (*Memory Leaks*)

Una **fuga de memoria** ocurre cuando se reserva memoria dinámica que sigue marcada como ocupada, pero el programa ha perdido toda referencia (puntero) para acceder a ella o liberarla.

```cpp
void funcion() {
    int* p = new int[1'000'000]; // Aproximadamente 4 MB reservados
} // Al salir, p se destruye y los 4 MB se pierden para siempre
```

* **Consecuencia:** Si la función se llama repetidamente, la memoria perdida se acumula, el consumo crece sin parar, el programa se ralentiza y finalmente `new` falla lanzando `std::bad_alloc`.

### Otra fuga clásica: perder la dirección al reasignar

```cpp
// INCORRECTO (Fuga de memoria)
int* p = new int{10};
p = new int{20}; // Se sobrescribe p; la dirección del 10 se pierde
delete p;        // Solo libera el 20

// CORRECTO
int* p = new int{10};
delete p;        // Liberamos primero el 10
p = new int{20};
delete p;        // Liberamos el 20
```
> **Regla:** Liberar siempre antes de reasignar un puntero que es el único acceso a un bloque dinámico.

### La solución: `delete`

```cpp
int* p = new int{10};
// ... uso del objeto ...
delete p;
```

Conceptualmente, `delete p;` realiza dos acciones en orden inverso a `new`:
1. **Invoca el destructor** del objeto apuntado.
2. **Libera el bloque de memoria** devolviéndolo a la *free store*.

> **Nota sobre destructores:** Los destructores no deben lanzar excepciones (si lo hicieran durante un `delete`, la liberación podría no completarse). Desde C++11, los destructores son `noexcept` por defecto.

### Punteros colgantes (*Dangling Pointers*)

Tras ejecutar `delete p;`, la variable `p` **sigue existiendo** y conserva la dirección antigua de memoria, que ahora ya no es válida. A esto se le llama **puntero colgante**. Usarlo provoca comportamiento indefinido.

```cpp
// INCORRECTO
delete p;
std::cout << *p; // Uso tras liberar (Use-after-free): UB

// BUENA PRÁCTICA
delete p;
p = nullptr;     // Deja explícito que p ya no apunta a nada válido
```

### La regla de oro del emparejamiento

| Reserva | Liberación correcta | Uso |
| :--- | :--- | :--- |
| `new X` | `delete p;` | Un único objeto. |
| `new X[n]` | `delete[] p;` | Un array de objetos. |

* **Mezclarlos** (por ejemplo, reservar con `new int[10]` y liberar con `delete p;`) es **comportamiento indefinido**.
* `delete[]` **no necesita recibir el tamaño `n`**: el sistema guarda internamente la información necesaria para destruir y liberar todo el array.

### C++ moderno: gestión automática (RAII)

En C++ moderno se reduce al mínimo el uso manual de `new` y `delete` utilizando herramientas que liberan la memoria automáticamente al salir de su ámbito, aunque entender `new`/`delete` es esencial para comprender cómo funcionan por dentro:

* **`std::unique_ptr`**: Un único propietario; libera el objeto al salir de su ámbito (`auto p = std::make_unique<int>(10);`).
* **`std::shared_ptr`**: Propiedad compartida; libera cuando desaparece el último propietario (`auto q = std::make_shared<int>(10);`).
* **`std::vector`**: Array dinámico que gestiona su propia memoria y crece automáticamente (`std::vector<int> v(n);`).

### Herramientas para detectar fugas de memoria

* **AddressSanitizer (`g++` / `clang++`):** `g++ -g -fsanitize=address prog.cpp` (detecta uso tras liberar, desbordamientos y fugas en Linux).
* **Valgrind (Memcheck - Linux):** `valgrind --leak-check=full ./prog` (indica cada bloque perdido y en qué línea se reservó).
* **macOS:** `leaks --atExit -- ./prog` o *Instruments (Leaks)* en Xcode.
* **Windows (Visual Studio):** `_CrtDumpMemoryLeaks();` en modo Debug.

---

## 4. Fragmentación de la memoria libre

### ¿Qué es la fragmentación?

La **fragmentación** ocurre cuando existe suficiente memoria libre en total, pero está repartida en bloques pequeños no contiguos que impiden realizar reservas de un tamaño mayor.

#### Ejemplo paso a paso (memoria total de 12 KiB)
1. **Inicio:** `[ LIBRE (12 KiB) ]` $\rightarrow$ 12 KiB libres.
2. **Reservamos A, B y C (4 KiB cada uno):** `[ A (4 KiB) | B (4 KiB) | C (4 KiB) ]` $\rightarrow$ 0 KiB libres.
3. **Liberamos A y C:** `[ LIBRE (4 KiB) | B (4 KiB) | LIBRE (4 KiB) ]` $\rightarrow$ 8 KiB libres en total.
4. **Pedimos 8 KiB contiguos:** **Falla.** Aunque hay 8 KiB libres en total, están divididos en dos huecos de 4 KiB separados por B.

*(Analogía del aparcamiento: hay 4 plazas libres alternadas entre coches ocupados, pero llega un camión que necesita 4 plazas seguidas y no puede aparcar).*

### Costes de la memoria dinámica y algoritmos de asignación

La memoria dinámica es flexible, pero no gratuita: requiere buscar espacio, mantener registros de bloques libres/ocupados, sufre fragmentación y puede fallar (`std::bad_alloc`).

Los gestores de memoria utilizan distintas estrategias clásicas para elegir un hueco:
* **First-fit:** Elige el primer hueco suficientemente grande. Es rápido.
* **Best-fit:** Elige el hueco más ajustado al tamaño pedido. Menos desperdicio inmediato, pero requiere más búsqueda y suele dejar huecos diminutos inservibles.
* **Worst-fit:** Elige el hueco más grande disponible, intentando dejar restos aprovechables.

### Estrategia de optimización: reservar una vez y reutilizar

Si el tamaño de un *buffer* es conocido y se va a usar muchas veces dentro de un bucle, es mucho más eficiente reservarlo una sola vez fuera del bucle que reservar y liberar en cada iteración:

```cpp
// PEOR PATRÓN: 100.000 reservas + 100.000 liberaciones
for (int k = 0; k < 100000; ++k) {
    int* buffer = new int[10000];
    // usamos el buffer
    delete[] buffer;
}

// ALTERNATIVA EFICIENTE: 1 reserva + 1 liberación
int* buffer = new int[10000];
for (int k = 0; k < 100000; ++k) {
    // reutilizamos el mismo buffer
}
delete[] buffer;
```

---

## 5. Aritmética de punteros

### Avanzar por elementos: `p + i`

Dado `int* p = new int[5];` (suponiendo `sizeof(int) == 4` bytes y dirección base `0x1000`):

```text
Dirección:  0x1000    0x1004    0x1008    0x100C    0x1010
Elemento:    [0]       [1]       [2]       [3]       [4]
Puntero:      p       p + 1     p + 2     p + 3     p + 4
```

* **`p + 1` NO suma 1 byte:** avanza **un elemento completo**, es decir, `sizeof(T)` bytes.
* La aritmética de punteros siempre avanza en unidades del tipo apuntado.

### Equivalencia fundamental: `*(p + i)` $\equiv$ `p[i]`

`p[i]` es, por definición en C++, una forma abreviada de escribir `*(p + i)`.

Si tenemos `int* p = new int[5]{10, 20, 30, 40, 50};`:

| Expresión | Significado | Resultado |
| :--- | :--- | :--- |
| `p` | Dirección del 1.er elemento | Dirección de `[0]` |
| `p + 1` | Dirección del 2.º elemento | Dirección de `[1]` |
| `*p` | 1.er elemento | `10` |
| `*(p + 1)` | 2.º elemento | `20` |
| `p[0]` | 1.er elemento | `10` |
| `p[2]` | 3.er elemento ($\equiv$ `*(p + 2)`) | `30` |

### Aritmética de punteros con estructuras

Dado `Student* p = new Student[100];`, para acceder al miembro `grade1` del quinto estudiante (índice `4`, ya que se empieza en `0`), las tres expresiones siguientes son **totalmente equivalentes**:

```cpp
(*(p + 4)).grade1 = 10.0; // Desreferenciar y acceder con punto
(p + 4)->grade1 = 10.0;   // p + 4 es un Student*, admite operador flecha ->
p[4].grade1 = 10.0;       // Notación de array (la más clara y habitual)
```

---

## 6. Síntesis y errores frecuentes

### Los 10 errores que hay que vigilar

1. **Confundir `int* p;` con `nullptr`:** Valor indeterminado $\neq$ puntero nulo.
2. **Creer que `new` crea el puntero:** `new` crea el objeto en la *free store*; el puntero `p` es otra variable (en el *stack*).
3. **Creer que al morir `p` muere el objeto:** Al salir del ámbito, el objeto dinámico sigue reservado.
4. **Olvidar `delete`:** Produce una fuga de memoria (*memory leak*).
5. **Confundir `delete` y `delete[]`:** Siempre `new` $\leftrightarrow$ `delete` y `new[]` $\leftrightarrow$ `delete[]`.
6. **Usar el puntero tras `delete`:** Puntero colgante (*dangling pointer*) $\rightarrow$ Comportamiento indefinido.
7. **Creer que `p + 1` avanza un byte:** Avanza un objeto completo (`sizeof(T)` bytes).
8. **Creer que `p[i]` no tiene relación con punteros:** `p[i]` $\equiv$ `*(p + i)`.
9. **Perder la dirección antes de liberar:** Reasignar `p = new ...` sin un `delete` previo.
10. **Creer que la memoria libre es ilimitada:** Se agota y se fragmenta.

### ¿Por qué no usar memoria dinámica para todo?

* La pila (*stack*) es más simple y rápida: las variables locales se gestionan solas.
* La memoria libre (*free store*) tiene coste de gestión, riesgo de fugas y riesgo de fragmentación.
* **Criterio general:** Usar la **pila** para variables locales de tamaño moderado; usar la **memoria libre** para objetos grandes, que deban sobrevivir a su ámbito o cuyo tamaño se decida/cambie en tiempo de ejecución.

---

## 7. Repaso práctico (Ejercicios clave resueltos)

### Ejercicio 1: Ejemplo integrador completo

```cpp
#include <iostream>

struct Product {
    int id;
    double price;
};

int main() {
    int n;
    std::cout << "Numero de productos: ";
    std::cin >> n;

    Product* products = new Product[n]; // Reserva dinámica en free store

    for (int i = 0; i < n; ++i) {
        products[i].id = i + 1;
        products[i].price = (i + 1) * 10.0;
    }

    for (int i = 0; i < n; ++i) {
        std::cout << "Producto " << (products + i)->id
                  << ": " << products[i].price << '\n';
    }

    delete[] products;   // Emparejado con new[]
    products = nullptr;  // Evita puntero colgante
}
```

**Puntos clave del código:**
* `products` vive en el *stack*; los `n` objetos `Product` viven en la *free store*.
* `new Product[n]` devuelve un puntero al primer elemento del array.
* `(products + i)->id`, `products[i].id` y `(*(products + i)).id` son equivalentes.

### Ejercicio 2: Detectar errores

```cpp
int* p = new int[5]{1, 2, 3, 4, 5};
std::cout << p[2] << '\n';
delete p;                   // ERROR 1: debe ser delete[] p;
std::cout << p[1] << '\n';  // ERROR 2: uso de puntero colgante tras liberar (UB)
```

### Preguntas rápidas de autoevaluación

1. **¿Diferencia entre `int* p;` e `int* p = nullptr;`?**  
   El primero tiene valor indeterminado; el segundo indica explícitamente que no apunta a nada.
2. **Con `int* p = new int[5];`, ¿qué es `p + 2` y a qué equivale `*(p + 2)`?**  
   `p + 2` es un puntero al tercer entero (índice 2); `*(p + 2)` equivale a `p[2]`.
3. **Con `Student* p = new Student[10];`, ¿cómo accedemos al nombre del 5.º estudiante?**  
   `p[4].name` (o `(p + 4)->name`).