#Muchas de las funcionalidades de la biblioteca no están bien implementadas, ya que permite ciertos comportamientos que realmente deberían ser errores. Vamos a enumerar algunas excepciones que se deberían implementar:

#Un libro no puede ser prestado de nuevo si ya tiene un préstamo en activo. Cuando ocurra, la excepción deberá devolver un error del tipo: "El libro xxxxx ya tiene un préstamo asociado en activo".
#Una persona no puede devolver un libro que no haya tomado prestado. Cuando ocurra, la excepción devolverá un mensaje del tipo "El libro xxxxx no ha sido prestado al usuario yyyyyyy".
#No se puede superar el máximo de libros prestados. En caso de que ocurra, la excepción será "El libro xxxx no puede prestarse a yyyy porque su máximo de préstamos es zzzz".

from datetime import date

"""
Clase Material y heredadas
"""
# Creación de la primera excepción
class PréstamoActivoException(Exception):
    def __init__(self, libro, *args):
        super().__init__(*args)
        self._libro = libro
    
    def __str__(self):
        return "El libro " + self._libro.título + " ya tiene un préstamo asociado en activo."
    
    
# Creación de la segunda excepción
class DevoluciónException(Exception):
    def __init__(self, libro, usuario, *args):
        super().__init__(*args)
        self._libro = libro
        self._usuario = usuario
    
    def __str__(self):
        return f"El libro {self._libro.título} no ha sido prestado al usuario {self._usuario.nombre}"
    
    
# Creación de la tercera excepción
class MaxPréstamosException(Exception):
    def __init__(self, libro, usuario, *args):
        super().__init__(*args)
        self._libro = libro
        self._usuario = usuario
    
    def __str__(self):
        return f"El libro {self._libro.título}  no puede prestarse a {self._usuario.nombre} porque su máximo de préstamos es {self._usuario._maxPrestamos}"

class Material:
    def __init__(self, título, código):
        self._título = título
        self._código = código
        self._prestado = False
    
    # Getters necesarios
    @property
    def título(self):
        return self._título
    
    @property
    def código(self):
        return self._código
    
    @property
    def prestado(self):
        return self._prestado
    
    def prestar(self):
        if self._prestado:
            raise PréstamoActivoException(self)
        self._prestado = True
        
    def devolver(self):
        self._prestado = False
        
        
class Libro(Material):
    def __init__(self, título, código, autor):
        # super() llama a la superclase Material, así que super().__init__ es el constructor
        # de la clase material
        super().__init__(título, código)
        self._autor = autor
        
class Revista(Material):
    def __init__(self, título, código, número, volumen):
        super().__init__(título, código)
        self._número = número
        self._volumen = volumen

"""
Clase Usuario y heredadas
"""
# Como aún no están declaradas y tenemos que dirigirnos a ellas, creamos una clase vacía
# Esto da igual a la hora de programar, pero VS Code nos va a dejar tranquilos y no va a subrayar
# cada aparición de Préstamo
class Préstamo: pass

class Usuario:
    def __init__(self, dni, nombre):
        self._dni = dni
        self._nombre = nombre
        self._prestamos = list()
        self._maxPrestamos = 0
        
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def maxPrestamos(self):
        return self._maxPrestamos
    
    # ATENCIÓN: esto es un getter de un atributo que no existe. Este es el verdadero potencial
    # de los getters y setters en Python   
    @property
    def num_prestamos(self):
        return len(self._prestamos)
    
    def realizaPrestamo(self, material: Material):
        # Retiramos la comprobación de aquí: ahora hay excepciones
        if self.maxPrestamos == self.num_prestamos:
            raise MaxPréstamosException(material, self)
        nuevo_préstamo = Préstamo(material, self)
        self._prestamos.append(nuevo_préstamo)
        return nuevo_préstamo
    
    def devuelve(self, material: Material):
        for i, p in enumerate(self._prestamos):
            if p.material.código == material.código:
                self._prestamos.pop(i)
                # En caso de que encontremos el libro, salimos del bucle y de la función
                return
        # Si hemos llegado aquí, se ha intentado devolver un libro no prestado
        raise DevoluciónException(material, self)
            
    
    
    
class Estudiante(Usuario):
    def __init__(self, dni, nombre, carrera, curso):
        super().__init__(dni, nombre)
        self._carrera = carrera
        self._curso = curso
        self._maxPrestamos = 5
        
class Profesor(Usuario):
    def __init__(self, dni, nombre, departamento):
        super().__init__(dni, nombre)
        self._departamento = departamento
        self._maxPrestamos = 10


"""
Clase Préstamo
"""
class Préstamo:
    def __init__(self, m: Material, u: Usuario):
        self._material = m
        self._usuario = u
        self._fechaInicio = date.today()
        self._fechaFin = None
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def material(self):
        return self._material
    
    def cerrarPréstamo(self):
        self._fechaFin = date.today()
        

"""
Clase Biblioteca
"""
class Biblioteca:
    def __init__(self):
        self._usuarios = list()
        self._prestamos = list()
        self._materiales = list()
    
    # Poner los tipos en los argumentos es opcional... pero VS Code nos ayuda a programar.
    # Por ejemplo, gracias a poner los tipos, cuando he escrito "préstamo = u." Python me ha dado
    # sugerencias (entre ellas realizaPrestamo)
    def prestar(self, u: Usuario, m: Material):
        préstamo = u.realizaPrestamo(m)
        if préstamo:
            self._prestamos.append(préstamo)
        m.prestar()
        return préstamo
        
    def devolver(self, p: Préstamo):
        p.usuario.devuelve(p.material)
        p.material.devolver()
        p.cerrarPréstamo()
        
    def añadir_usuario(self, u: Usuario):
        self._usuarios.append(u)
        
    def añadir_material(self, m: Material):
        self._materiales.append(m)
        
# Código de prueba para ver que todo funciona correctamente
if __name__ == '__main__':
    biblio = Biblioteca()
    
    users = [Profesor('1234K', 'David', 'Nebrija'),
             Estudiante('9876L', 'Alberto', 'Informática', '1'),
             Estudiante('4477Y', 'Laura', 'Informática', '3')]
    
    materiales = [Libro('Learning Python', '123456', 'Mark Lutz'),
                  Libro('100 años de soledad', '567890', 'Gabriel García Márquez'),
                  Revista('Muy interesante', '33445566', '16', '4'),
                  Libro('Carrie', '122223456', 'Stephen King'),
                  Libro('El médico', '12', 'Noah Gordon'),
                  Libro('Hamlet', '1233', 'William Shakespeare')]
    
    for user in users:
        biblio.añadir_usuario(user)
    
    for material in materiales:
        biblio.añadir_material(material)
    
    p = biblio.prestar(users[0], materiales[1])
    print('Libros prestados:', users[0].num_prestamos)
    
    # Descomentar esta línea para que salte la primera excepción
    # biblio.prestar(users[0], materiales[1])
    
    # Descomentar esta línea para que salte la segunda excepción
    # users[1].devuelve(materiales[0])
    
    biblio.devolver(p)
    # Descomentar estas líneas para la tercera excepción: seis libros no pueden prestarse a un alumno
    # for material in materiales:
    #     users[1].realizaPrestamo(material)
    
    