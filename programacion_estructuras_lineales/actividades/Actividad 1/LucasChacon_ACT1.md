## 1. Variables

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `libro1` … `libro20` | `Libro` | Los 20 ejemplares: ID, título, autor y categoría. |
| `usuario1`, `usuario2` | `Usuario` | Usuarios de prueba |
| `usuarios` | `Usuario[2]` | Array de usuario que reciben las funciones. |
| `libros` | `Libro[20]` | Array de libros que reciben las funciones. |
| `condition` | `bool` | Controla el bucle del menú, en `false` sale. |
| `opcion` | `int` | Opción elegida en el menú. |
| `idLibro`, `dniUsuario` | `string` | Claves de búsqueda introducidas por teclado. |

Inicialización en `main`:

```cpp
Libro libro1("1", "El Señor de los Anillos", "J.R.R. Tolkien", Categoria::Aventura);
Libro libro2("2", "1984", "George Orwell", Categoria::Drama);
// ... hasta libro20

Usuario usuario1("Lucas", "Chacón", "12345678A");
Usuario usuario2("María", "García", "87654321B");

Usuario usuarios[2] = {usuario1, usuario2};
Libro libros[20] = {libro1, libro2, /* ... */, libro20};
```

---

## 2. Clases

### 2.1 enum class Categoria

```cpp
enum class Categoria {
    Acción,     
    Aventura,  
    Drama,      
    Comedia,   
    Romanticismo, 
    Fantasía    
};
```

Sólo se puede asignar a un `Categoria` uno de los seis valores listados. Cada valor tiene un entero implícito del 0 al 5 en el orden en que se declaran. En el catálogo se usa con el prefijo `Categoria::`, por ejemplo `Categoria::Aventura`.

### 2.2 Clase Libro

```cpp
class Libro {
    private:
        std::string idLibro;
        std::string titulo;
        std::string autor;
        Categoria categoria;
        bool disponible;

    public:
        Libro(){};
        Libro(std::string i, std::string t, std::string a, Categoria c)
            : idLibro(i), titulo(t), autor(a), categoria(c), disponible(true) {}

        std::string getId() const { return idLibro; }
        std::string getTitulo() const { return titulo; }
        std::string getAutor() const { return autor; }
        Categoria getCategoria() const { return categoria; }
        bool isDisponible() const { return disponible; }

        void setDisponible(bool d) { disponible = d; }
};
```

**Atributos (sección `private`):**

| Atributo | Tipo | Descripción |
| --- | --- | --- |
| `idLibro` | `std::string` | Identificador único del ejemplar en el catálogo ("1", "2" … "20"). Es la clave con la que se buscan los libros en todas las funciones. |
| `titulo` | `std::string` | Título del libro. Es lo que se imprime en las listas de reservas e historial. |
| `autor` | `std::string` | Nombre del autor de la obra. Se almacena en el objeto aunque no se muestre en el menú. |
| `categoria` | `Categoria` | Categoría a la que pertenece (acción, aventura, drama, comedia, romanticismo, fantasía), definida con el enumerado. |
| `disponible` | `bool` | Estado del préstamo: `true` = libre en el catálogo, `false` = prestado a un usuario. Se inicializa en `true` con el constructor con parámetros. |

**Constructores:**

- `Libro(){}` — constructor por defecto. No asigna valores, así que el objeto queda con `idLibro` vacío. Es el que usa `unsetLibrosReservados` para dejaruna casilla de reserva "en blanco", y el que generan los arrays sin inicializar.
- `Libro(i, t, a, c)` — constructor con parámetros. Recibe los cuatro datos del ejemplar con el operador de inicialización de miembros (`:`) y deja `disponible` en `true` por defecto (un libro recién creado está libre).

**Métodos de lectura (getters, marcados `const` porque sólo leen):**

- `getId()`  devuelve `idLibro`. Clave de búsqueda en `existeLibro`,
`libroDisponible`, `asignarLibro` y `desasignarLibro`.
- `getTitulo()`  devuelve `titulo`. Es el que se muestra en `getUsuarioReservas` y `getUsuarioHistorial`.
- `getAutor()`  devuelve `autor`. Expone el autor aunque el menú no lo imprima.
- `getCategoria()`  devuelve `categoria` como tipo `Categoria`. Expone la clasificación de la obra.
- `isDisponible()`  devuelve `disponible`. Es la base de `libroDisponible()` y de `disponibilidadLibros()`.

**Métodos de escritura (setter):**

- `setDisponible(bool d)`  es el único que modifica el objeto desde fuera. `asignarLibro` lo llama con `false` al prestar; `desasignarLibro` lo llama con `true` al devolver.

### 2.3 Clase Usuario

```cpp
class Usuario {
    private:
        std::string nombre;
        std::string apellidos;
        std::string dni;
        std::array<Libro, 5> librosReservados;
        std::array<Libro, 10> historialLibros;

    public:
        Usuario(std::string n, std::string a, std::string d)
            : nombre(n), apellidos(a), dni(d) {}

        std::string getNombre() const { return nombre; }
        std::string getApellidos() const { return apellidos; }
        std::string getDni() const { return dni; }
        std::array<Libro, 5> getLibrosReservados() { return librosReservados; }
        std::array<Libro, 10> getHistorialLibros() { return historialLibros; }

        void setLibrosReservados(Libro libro) {
            for (int i = 0; i < librosReservados.size(); i++) {
                if (librosReservados[i].getId().empty()) {
                    librosReservados[i] = libro;
                    break;
                }
            }
        }

        void unsetLibrosReservados(Libro libro) {
            for (int i = 0; i < librosReservados.size(); i++) {
                if (librosReservados[i].getId() == libro.getId()) {
                    librosReservados[i] = Libro(); // deja la casilla vacía
                    break;
                }
            }
        }

        void setHistorialLibros(Libro libro) {
            for (int i = 0; i < historialLibros.size(); i++) {
                if (historialLibros[i].getId().empty()) {
                    historialLibros[i] = libro;
                    break;
                }
            }
        }
};
```

**Atributos (sección `private`):**

| Atributo | Tipo | Descripción |
| --- | --- | --- |
| `nombre` | `std::string` | Nombre de pila del usuario. Se rellena en el constructor y se lee con `getNombre()`. |
| `apellidos` | `std::string` | Apellidos del usuario. Se rellena en el constructor y se lee con `getApellidos()`. |
| `dni` | `std::string` | DNI del usuario. Es la clave de búsqueda: con él se recorre el padrón en `existeUsuario`, `espacioUsuario`, `asignarLibro`, `desasignarLibro`, `getUsuarioReservas` y `getUsuarioHistorial`. |
| `librosReservados` | `std::array<Libro, 5>` | Lista de libros que el usuario tiene prestados ahora mismo. Cabe un máximo de 5 ejemplares a la vez. Las casillas empiezan con el ID vacío (constructor por defecto de `Libro`); una casilla con `idLibro` vacío significa que está libre. |
| `historialLibros` | `std::array<Libro, 10>` | Registro histórico de todos los libros que el usuario ha tenido, tanto si aún los tiene como si ya los devolvió. Cabe un máximo de 10 entradas. Al igual que las reservas, se marca con el ID vacío en las posiciones sin usar. |

**Constructor:**

- `Usuario(n, a, d)` recibe nombre, apellidos y DNI con el operador de inicialización de miembros (`:`). No recibe los arrays: `librosReservados` e `historialLibros` se crean vacíos de forma automática (todos los `Libro` con ID en blanco), listos para que `setLibrosReservados` y
`setHistorialLibros` inserten en la primera posición libre.

**Métodos de lectura (getters):**

- `getNombre()` devuelve `nombre` (const).
- `getApellidos()`  devuelve `apellidos` (const).
- `getDni()`  devuelve `dni` (const). Clave con la que se identifica al
usuario en todas las funciones.
- `getLibrosReservados()`  devuelve una **copia** del array completo de 5 reservas. Por eso desde fuera no se pueden modificar las reservas directamente; sólo a través de `setLibrosReservados` /
`unsetLibrosReservados`.
- `getHistorialLibros()`  devuelve una **copia** del array completo de 10 entradas de historial. Mismo criterio: lectura desde fuera, escritura sólo con `setHistorialLibros`.

**Métodos de escritura:**

- `setLibrosReservados(Libro libro)` recorre `librosReservados` buscando la primera casilla cuyo ID esté vacío (`getId().empty()`) y guarda ahí el libro recibido. Rompe el bucle en cuanto inserta (hueco libre). Si las 5 casillas están ocupadas, no hace nada.
- `unsetLibrosReservados(Libro libro)` recorre `librosReservados` buscando la casilla cuyo ID coincida con el del libro recibido y la sustituye por un `Libro()` vacío, es decir, borra esa reserva y deja la casilla disponible de nuevo.
- `setHistorialLibros(Libro libro)` mismo criterio que `setLibrosReservados`, pero sobre `historialLibros`: inserta en la primera casilla con ID vacío. El historial no tiene método de borrado: una vez registrado, el título queda para siempre.

---

## 3. Funciones auxiliares

Son helpers que devuelven `bool` o consultan datos sin pedir nada por teclado. Las usan las funciones principales para validar antes de actuar.

### 3.1 existeUsuario

```cpp
bool existeUsuario(Usuario usuarios[2], std::string dni) {
    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dni) {
            return true;
        }
    }
    return false;
}
```

Recorre el padrón comparando el DNI. Devuelve `true` si lo encuentra y `false` si llega al final sin hallarlo.

### 4.2 existeLibro

```cpp
bool existeLibro(Libro libros[20], std::string id) {
    for (int i = 0; i < 20; i++) {
        if (libros[i].getId() == id) {
            return true;
        }
    }
    return false;
}
```

Mismo criterio que la anterior, pero comparando el ID contra el catálogo.

### 3.3 libroDisponible

```cpp
bool libroDisponible(Libro libros[20], std::string id) {
    for (int i = 0; i < 20; i++) {
        if (libros[i].getId() == id) {
            return libros[i].isDisponible();
        }
    }
    return false;
}
```

Busca el libro por ID y devuelve su estado. Si el libro no está en el catálogo, devuelve `false`.

### 3.4 espacioUsuario

```cpp
bool espacioUsuario(Usuario usuarios[2], std::string dniUsuario) {
    int cont = 0;
    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < usuarios[i].getLibrosReservados().size(); j++) {
                if (usuarios[i].getLibrosReservados()[j].getId().empty()) {
                    cont++;
                }
            }
        }
    }
    if (cont == 0) {
        return false;
    }
    return true;
}
```

Cuenta las posiciones vacías del array de reservas del usuario. Si el contador es 0, no cabe un libro más y devuelve `false`.

---

## 4. Funciones principales

Son las que se invocan desde el menú. Piden datos por teclado, validan con las auxiliares y modifican los arrays.

### 4.1 disponibilidadLibros (opción 5)

```cpp
void disponibilidadLibros(Libro libros[20]) {
    std::string idLibro;
    std::cout << "Introduce el ID del libro para verificar su disponibilidad: ";
    std::cin >> idLibro;

    if (!existeLibro(libros, idLibro)) {
        std::cout << "El libro '" << idLibro << "' no existe." << std::endl;
        return;
    }

    for (int i = 0; i < 20; i++) {
        if (libros[i].getId() == idLibro) {
            if (libros[i].isDisponible()) {
                std::cout << "El libro '" << idLibro << "' está disponible." << std::endl;
            } else {
                std::cout << "El libro '" << idLibro << "' no está disponible." << std::endl;
            }
            return;
        }
    }
}
```

Pide el ID. Primero valida con `existeLibro`; si no existe, avisa y sale. Después recorre el catálogo y muestra si `isDisponible()` es `true` o `false`.

### 4.2 getUsuarioReservas (opción 3)

```cpp
std::array<Libro, 5> getUsuarioReservas(Usuario usuarios[2]) {
    std::string dniUsuario;
    std::cout << "Introduce el DNI del usuario para ver su historial: ";
    std::cin >> dniUsuario;

    if (!existeUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no existe." << std::endl;
        return std::array<Libro, 5>();
    }

    if (!espacioUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no tiene espacio para más libros." << std::endl;
        return std::array<Libro, 5>();
    }

    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < usuarios[i].getLibrosReservados().size(); j++) {
                std::cout << "- " << usuarios[i].getLibrosReservados()[j].getTitulo() << std::endl;
            }
            return usuarios[i].getLibrosReservados();
        }
    }
    return std::array<Libro, 5>();
}
```

Pide el DNI y valida con `existeUsuario` y con `espacioUsuario`. Si todo va bien, imprime el título de cada reserva y devuelve el array. Si algo falla, devuelve un array por defecto con los IDs vacíos.

### 4.3 getUsuarioHistorial (opción 4)

```cpp
std::array<Libro, 10> getUsuarioHistorial(Usuario usuarios[2]) {
    std::string dniUsuario;
    std::cout << "Introduce el DNI del usuario para ver su historial: ";
    std::cin >> dniUsuario;

    if (!existeUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no existe." << std::endl;
        return std::array<Libro, 10>();
    }

    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < usuarios[i].getHistorialLibros().size(); j++) {
                std::cout << "- " << usuarios[i].getHistorialLibros()[j].getTitulo() << std::endl;
            }
            return usuarios[i].getHistorialLibros();
        }
    }
    return std::array<Libro, 10>();
}
```

Igual que la anterior, pero lista el historial (todos los libros que el
usuario ha tenido alguna vez, aunque los haya devuelto). Sólo valida con
`existeUsuario`.

### 4.4 asignarLibro (opción 1 — sacar un libro)

```cpp
void asignarLibro(Usuario usuarios[2], Libro libros[20]) {
    std::string dniUsuario;
    std::cout << "Ingrese el DNI del usuario: ";
    std::cin >> dniUsuario;

    if (!existeUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no existe." << std::endl;
        return;
    }

    std::string idLibro;
    std::cout << "Ingrese el ID del libro a asignar: ";
    std::cin >> idLibro;

    if (!existeLibro(libros, idLibro)) {
        std::cout << "El libro con ID '" << idLibro << "' no existe." << std::endl;
        return;
    }

    if (!libroDisponible(libros, idLibro)) {
        std::cout << "El libro con ID '" << idLibro << "' no está disponible." << std::endl;
        return;
    }

    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < 20; j++) {
                if (libros[j].getId() == idLibro) {
                    usuarios[i].setLibrosReservados(libros[j]);
                    usuarios[i].setHistorialLibros(libros[j]);
                    libros[j].setDisponible(false);
                    break;
                }
            }
            break;
        }
    }

    std::cout << "El libro '" << idLibro << "' ha sido asignado a " << dniUsuario << "." << std::endl;
}
```

Procedimiento paso a paso:

1. Pide el DNI y valida con `existeUsuario`.
2. Pide el ID del libro y valida con `existeLibro`.
3. Comprueba con `libroDisponible` que el libro esté libre.
4. Recorre `usuarios` buscando el DNI y, dentro, `libros` buscando el ID.
5. Cuando los encuentra:
    - `setLibrosReservados()` → lo añade a la reserva del usuario.
    - `setHistorialLibros()` → lo deja registrado en el historial.
    - `setDisponible(false)` → lo marca como prestado.
6. Muestra el mensaje de confirmación.

### 5.5 desasignarLibro (opción 2 — devolver un libro)

```cpp
void desasignarLibro(Usuario usuarios[2], Libro libros[20]) {
    std::string dniUsuario;
    std::cout << "Ingrese el DNI del usuario: ";
    std::cin >> dniUsuario;

    if (!existeUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no existe." << std::endl;
        return;
    }

    std::string idLibro;
    std::cout << "Ingrese el ID del libro a devolver: ";
    std::cin >> idLibro;

    if (!existeLibro(libros, idLibro)) {
        std::cout << "El libro con ID '" << idLibro << "' no existe." << std::endl;
        return;
    }

    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < 20; j++) {
                if (libros[j].getId() == idLibro) {
                    usuarios[i].unsetLibrosReservados(libros[j]);
                    libros[j].setDisponible(true);
                    break;
                } else {
                    std::cout << "El libro con ID '" << idLibro
                              << "' no está asignado a " << dniUsuario << "." << std::endl;
                    return;
                }
            }
            break;
        }
    }
    std::cout << "El libro '" << idLibro << "' ha sido devuelto por " << dniUsuario << "." << std::endl;
}
```

Misma estructura que la anterior, pero al encontrar el libro:

1. `unsetLibrosReservados()` → quita el libro de la reserva (deja la casilla con `Libro()` vacío).
2. `setDisponible(true)` → lo devuelve al catálogo como disponible.
3. Muestra el mensaje de confirmación.

Si el libro no está en esa posición, avisa de que no está asignado al usuario.

---

## 5. Main

`main` crea los 20 libros y los 2 usuarios, los guarda en los arrays, y entra en un bucle que pinta el menú y despacha la opción con un `switch`:

```cpp
int main(int argc, char const *argv[]){
    // ... inicialización de libro1..libro20, usuario1, usuario2 ...

    Usuario usuarios[2] = {usuario1, usuario2};
    Libro libros[20] = {libro1, libro2, /* ... */, libro20};

    bool condition = true;

    while (condition)
    {
        std::cout << "-------------------------" << std::endl;
        std::cout << "Menu" << std::endl;
        std::cout << "1. Reservar libro" << std::endl;
        std::cout << "2. Devolver libro" << std::endl;
        std::cout << "3. Reservas de usuarios" << std::endl;
        std::cout << "4. Historial de usuarios" << std::endl;
        std::cout << "5. Comprobar disponibilidad de libro" << std::endl;
        std::cout << "6. Salir" << std::endl;

        int opcion;
        std::cout << "Seleccione una opción: ";
        std::cin >> opcion;

        switch (opcion)
        {
        case 1:
            asignarLibro(usuarios, libros);
            break;
        case 2:
            desasignarLibro(usuarios, libros);
            break;
        case 3:
            std::cout << "Reservas de usuarios:" << std::endl;
            getUsuarioReservas(usuarios);
            break;
        case 4:
            std::cout << "Historial de usuarios:" << std::endl;
            getUsuarioHistorial(usuarios);
            break;
        case 5:
            std::cout << "Disponibilidad de libro:" << std::endl;
            disponibilidadLibros(libros);
            break;
        case 6:
            std::cout << "Hasta luego";
            condition = false;
            break;
        default:
            std::cout << "Opción no válida." << std::endl;
        }
    }

    return 0;
}
```