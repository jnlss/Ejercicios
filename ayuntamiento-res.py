#Ejercicio 1: Creación de un sistema de pagos de un ayuntamiento

#Diseña una aplicación para un ayuntamiento donde se puedan efectuar y registrar pagos. Para ello, se deben registrar unos ciertos usuarios, que podrán ser ciudadanos normales que quieran pagar sus impuestos o funcionarios que sean capaces de eliminar o crear nuevos pagos. Los pagos tendrán un importe, una fecha de creación, un estado "Pago pendiente" o "Finalizado", además de una fecha de pago en el caso de que se hayan finalizado. Desde el ayuntamiento se debe poder hacer, como mínimo:
#Dar de alta o de baja a nuevos usuarios y funcionarios.
#Creación y eliminación de pagos, siempre a través de un cierto funcionario.
#Listar todos los pagos, pudiendo filtrar por ciudadano, por fecha de inicio (indica un cierto intervalo), por fecha de fin (indica un cierto intervalo). También se pueden combinar estos filtros.

#Ejercicio 2: Excepciones
#Piensa e implementa al menos dos excepciones para este programa.

from datetime import datetime, MAXYEAR, MINYEAR, date, timedelta

class Usuario:
    def __init__(self, dni, nombre):
        self._dni = dni
        self._nombre = nombre
        
    @property
    def dni(self):
        return self._dni
    
class Pago:
    pass
        

class Ciudadano(Usuario):
    def __init__(self, dni, nombre):
        super().__init__(dni, nombre)
        self._pagos = list()

    def añade_pago(self, pago: Pago):
        self._pagos.append(pago)

class Funcionario(Usuario):
    def __init__(self, dni, nombre):
        super().__init__(dni, nombre)

class Pago:
    # Variable estática: existe una sola vez en la clase
    num_pagos = 0
    
    def __init__(self, importe: float, ciudadano: Ciudadano, funcionario: Funcionario):
        Pago.num_pagos += 1
        self._id = Pago.num_pagos
        self._importe = importe
        self._ciudadano = ciudadano
        self._fechaInicio = datetime.now().date()
        self._fechaPago = None
        self._creador = funcionario
        ciudadano.añade_pago(self)
        
    @property
    def ciudadano(self):
        return self._ciudadano
    
    @property
    def id(self):
        return self._id
    
    @property
    def fechaInicio(self):
        return self._fechaInicio
    
    @property
    def fechaPago(self):
        return self._fechaPago
    
    @property
    def estado(self):
        if self._fechaPago:
            return "Finalizado"
        else:
            return "Pago pendiente"
    
    def pagar(self):
        self._fechaPago = datetime.now().date()

class Ayuntamiento:
    def __init__(self):
        self._listaCiudadanos = list()
        self._listaFuncionarios = list()
        self._listaPagos = list()
        
    def crearUsuario(self, u: Usuario):
        # Esta función evalúa si un cierto objeto es de una cierta clase
        if isinstance(u, Funcionario):
            self._listaFuncionarios.append(u)
        elif isinstance(u, Ciudadano):
            self._listaCiudadanos.append(u)
    
    def bajaUsuario(self, dni):
        for i, u in enumerate(self._listaCiudadanos):
            if u.dni == dni:
                self._listaCiudadanos.pop(i)
                return
            
        for i, u in enumerate(self._listaFuncionarios):
            if u.dni == dni:
                self._listaFuncionarios.pop(i)
                return
    
    def crearPago(self, importe, dni, funcionario: Funcionario):
        user = None
        for u in self._listaCiudadanos:
            if u.dni == dni:
                user = u
                break
        pago = Pago(importe, user, funcionario)
        self._listaPagos.append(pago)
        
    def eliminaPago(self, id, funcionario: Funcionario):
        for i, p in enumerate(self._listaPagos):
            if p.id == id:
                self._listaPagos.pop(i)
    
    def listarPagos(self, dni=None,
                    fechaInicioCreación=date(year=MINYEAR, month=1, day=1),
                    fechaFinCreación=date(year=MAXYEAR, month=12, day=31),
                    fechaInicioPago=date(year=MINYEAR, month=1, day=1),
                    fechaFinPago=date(year=MAXYEAR, month=12, day=31)):
        
        def filtroDni(pago: Pago):
            if dni: 
                return pago.ciudadano.dni == dni
            else:
                return True
        
        def filtroCreación(pago: Pago):
            return fechaInicioCreación <= pago.fechaInicio <= fechaFinCreación
        
        def filtroPago(pago: Pago):
            # Nos aseguramos de que exista una fecha de pago
            return (pago.fechaPago is None) or fechaInicioPago <= pago.fechaPago <= fechaFinPago
        
        return list(filter(filtroPago, filter(filtroCreación, filter(filtroDni, self._listaPagos))))
    
if __name__ == '__main__':
    # Creamos el ayuntamiento
    a = Ayuntamiento()

    # Creamos usuarios
    c1 = Ciudadano('32421435K', 'David')
    c2 = Ciudadano('11111111W', 'José')
    f1 = Funcionario('09876543A', 'María')

    # Los registramos en el ayuntamiento
    a.crearUsuario(c1)
    a.crearUsuario(c2)
    a.crearUsuario(f1)

    # Creamos algunos pagos
    a.crearPago(150.0, '32421435K', f1)
    a.crearPago(200.0, '32421435K', f1)
    a.crearPago(300.0, '11111111W', f1)
    
    # Marcamos uno como pagado
    a._listaPagos[0].pagar()
    
    # Eliminamos uno (por ID)
    id_a_eliminar = a._listaPagos[1].id
    a.eliminaPago(id_a_eliminar, f1)
    
    print("Pagos realizados en los últimos 2 días:")
    fecha_inicio = (datetime.now() - timedelta(days=2)).date()
    fecha_fin = datetime.now().date()
    for p in a.listarPagos(fechaInicioPago=fecha_inicio, fechaFinPago=fecha_fin):
        print(f"  ID {p.id}: ciudadano {p._ciudadano._nombre}, pagado el {p.fechaPago}")