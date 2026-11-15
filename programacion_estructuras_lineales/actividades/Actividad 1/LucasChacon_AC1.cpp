/*
La actividad 1, consiste en implementar el sistema digital de gestión de libros de
una biblioteca pública.
Para su entrega deben cumplirse las siguientes condiciones:
• La actividad se desarrollará individualmente.
• La entrega se realizará mediante el campus virtual.
• Tendréis que incluir un video donde compartiendo pantalla expliquéis el
código correspondiente al desarrollo que habéis realizado como solución del
ejercicio propuesto.
• Para terminar, deberá realizarse una memoria sobre las actividades
realizadas, explicando los procedimientos, funciones, variables, etc. Dicha
memoria se llamará “Nombre_AC1.pdf”.
• En el documento debe encontrarse una explicación de la teoría estudiada
dentro de la asignatura y su implantación en el código. Así como un pequeño
manual de uso del programa en cuestión.


Enunciado
Una Biblioteca pretende crear un software para gestionar la entrada/salida de sus
libros ya que, su logística todavía se escribe en ficheros Excel de Windows XP (lo
cual en si ya es un avance a nivel logístico, pero resulta difícil gestionar los datos de
entrada y salida y el ordenador de la biblioteca no da más de sí.
Así pues, la biblioteca nos pide las siguientes funcionalidades:

• Tener una el sistema de la biblioteca con al menos 20 ejemplares separados
por categorías (acción, aventuras, drama, comedia, romanticismo...).
• Tener control de qué libros están o no disponibles y en caso negativo saber
quién lo tiene.
• Tener un registro de usuarios con sus datos y el historial de lectura:
o Nombre, Apellidos, DNI…
o Lista de libros reservados actualmente.
o Historial de libros reservados
Todo ese software pretende facilitarle la vida a los bibliotecarios que hacen las
gestiones de reservas de libros y les tiene que permitir realizar las siguientes
acciones:
• Comprobar qué libros hay disponibles
• Ver el historial de libros de una persona
• Ver si una persona tiene un libro o no
• Sacar un libro (asignárselo a una persona)
• Devolver un libro (desasignárselo a dicha persona)
*/

#include <iostream>
#include <string>
#include <array>

enum class Categoria {
    Acción,
    Aventura,
    Drama,
    Comedia,
    Romanticismo,
    Fantasía
};

class Libro {
    private:
        std::string idLibro;
        std::string titulo;
        std::string autor;
        Categoria categoria;
        bool disponible;


    public:
        Libro(){};
        Libro(std::string i, std::string t, std::string a, Categoria c) : idLibro(i), titulo(t), autor(a), categoria(c), disponible(true) {}

        std::string getId() const { return idLibro; }
        std::string getTitulo() const { return titulo; }
        std::string getAutor() const { return autor; }
        Categoria getCategoria() const { return categoria; }
        bool isDisponible() const { return disponible; }

        void setDisponible(bool d) { disponible = d; }
        

};

class Usuario {
    private:
        std::string nombre;
        std::string apellidos;
        std::string dni;
        std::array<Libro, 5> librosReservados; // Suponiendo un máximo de 5
        std::array<Libro, 10> historialLibros; // Suponiendo un máximo de 10

    public:
        Usuario(std::string n, std::string a, std::string d) : nombre(n), apellidos(a), dni(d) {}
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
                    librosReservados[i] = Libro(); // Asignar un libro vacío
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



bool existeUsuario(Usuario usuarios[2], std::string dni) {
    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dni) {
            return true;
        }
    }
    return false;
}

bool existeLibro(Libro libros[20], std::string id) {
    for (int i = 0; i < 20; i++) {
        if (libros[i].getId() == id) {
            return true;
        }
    }
    return false;
}

bool libroDisponible(Libro libros[20], std::string id) {
    for (int i = 0; i < 20; i++) {
        if (libros[i].getId() == id) {
            return libros[i].isDisponible();
        }
    }
    return false;
}

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
    std::cout << "El libro '" << idLibro << "' no existe." << std::endl;
}

std::array<Libro, 5> getUsuarioReservas(Usuario usuarios[2]) {
    std::string dniUsuario;
    std::cout << "Introduce el DNI del usuario para ver su historial: ";
    std::cin >> dniUsuario;

    if (!existeUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no existe." << std::endl;
        return std::array<Libro, 5>(); // Devolver un array vacío si no se encuentra el usuario
    }

    if (!espacioUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no tiene espacio para más libros." << std::endl;
        return std::array<Libro, 5>(); // Devolver un array vacío si el usuario no tiene libros reservados
    }


    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < usuarios[i].getLibrosReservados().size(); j++) {
                std::cout << "- " << usuarios[i].getLibrosReservados()[j].getTitulo() << std::endl;
            }
            return usuarios[i].getLibrosReservados();
        }
    }
    return std::array<Libro, 5>(); // Devolver un array vacío si no se encuentra el usuario
}

std::array<Libro, 10> getUsuarioHistorial(Usuario usuarios[2]) {
    std::string dniUsuario;
    std::cout << "Introduce el DNI del usuario para ver su historial: ";
    std::cin >> dniUsuario;

    if (!existeUsuario(usuarios, dniUsuario)) {
        std::cout << "El usuario con DNI '" << dniUsuario << "' no existe." << std::endl;
        return std::array<Libro, 10>(); // Devolver un array vacío si no se encuentra el usuario
    }

    for (int i = 0; i < 2; i++) {
        if (usuarios[i].getDni() == dniUsuario) {
            for (int j = 0; j < usuarios[i].getHistorialLibros().size(); j++) {
                std::cout << "- " << usuarios[i].getHistorialLibros()[j].getTitulo() << std::endl;
            }
            return usuarios[i].getHistorialLibros();
        }
    }
    return std::array<Libro, 10>(); // Devolver un array vacío si no se encuentra el usuario
}

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
                }else {
                    std::cout << "El libro con ID '" << idLibro << "' no está asignado a " << dniUsuario << "." << std::endl;
                    return;
                }
            }
            break;
        }
    }
    std::cout << "El libro '" << idLibro << "' ha sido devuelto por " << dniUsuario << "." << std::endl;
}


int main(int argc, char const *argv[]){
    Libro libro1("1", "El Señor de los Anillos", "J.R.R. Tolkien", Categoria::Aventura);
    Libro libro2("2", "1984", "George Orwell", Categoria::Drama);
    Libro libro3("3", "Orgullo y Prejuicio", "Jane Austen", Categoria::Romanticismo);
    Libro libro4("4", "Harry Potter y la Piedra Filosofal", "J.K. Rowling", Categoria::Fantasía);
    Libro libro5("5", "El Código Da Vinci", "Dan Brown", Categoria::Comedia);
    Libro libro6("6", "Cien Años de Soledad", "Gabriel García Márquez", Categoria::Fantasía);
    Libro libro7("7", "El Gran Gatsby", "F. Scott Fitzgerald", Categoria::Drama);
    Libro libro8("8", "La Sombra del Viento", "Carlos Ruiz Zafón", Categoria::Drama);
    Libro libro9("9", "El Hobbit", "J.R.R. Tolkien", Categoria::Aventura);
    Libro libro10("10", "Matar a un Ruiseñor", "Harper Lee", Categoria::Drama);
    Libro libro11("11", "El Principito", "Antoine de Saint-Exupéry", Categoria::Fantasía);
    Libro libro12("12", "Don Quijote de la Mancha", "Miguel de Cervantes", Categoria::Aventura);
    Libro libro13("13", "La Divina Comedia", "Dante Alighieri", Categoria::Acción);
    Libro libro14("14", "El Alquimista", "Paulo Coelho", Categoria::Comedia);
    Libro libro15("15", "La Metamorfosis", "Franz Kafka", Categoria::Acción);
    Libro libro16("16", "El Retrato de Dorian Gray", "Oscar Wilde", Categoria::Acción);
    Libro libro17("17", "El Nombre de la Rosa", "Umberto Eco", Categoria::Comedia);
    Libro libro18("18", "El Diario de Ana Frank", "Ana Frank", Categoria::Drama);
    Libro libro19("19", "El Viejo y el Mar", "Ernest Hemingway", Categoria::Drama);
    Libro libro20("20", "El Código Da Vinci", "Dan Brown", Categoria::Comedia);

    Usuario usuario1("Lucas", "Chacón", "12345678A");
    Usuario usuario2("María", "García", "87654321B");

    Usuario usuarios[2] = {usuario1, usuario2};
    Libro libros[20] = {libro1, libro2, libro3, libro4, libro5, libro6, libro7, libro8, libro9, libro10,
                      libro11, libro12, libro13, libro14, libro15, libro16, libro17, libro18, libro19, libro20};
    
    bool condition = true;
    
    while (condition)
    {
        std::cout << "-------------------------" <<std::endl;
        std::cout << "Menu" << std::endl;
        std::cout << "1. Reservar libro" << std::endl;
        std::cout << "2. Devolver libro" << std::endl;
        std::cout << "3. Reservas de usuarios" <<std::endl;
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
            getUsuarioReservas(usuarios);
            break;
        case 4:
            getUsuarioHistorial(usuarios);
            break;
        case 5:
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
