#Ejercicio 2: Comprobación de argumentos con una función arbitraria
#Crea un decorador @validate_arguments(checker) que recibe un parámetro checker. Esta función es una comprobación que devuelve True o False. Si alguno de los argumentos de la función encapsulada por el decorador no cumple la condición checker, se debe devolver ValueError.

def validate_arguments(checker):
    
    def decorador(función_genérica):
        
        def wrapper(*args, **kwargs):
            for argumento in args:
                assert checker(argumento), ValueError
                
            for values in kwargs.values():
                assert checker(values), ValueError
            
            return función_genérica(*args, **kwargs)
        
        return wrapper
    
    return decorador

def check(arg):
    if type(arg) == str:
        return True
    else:
        return False


@validate_arguments(check)
def suma(a, b, num_opcional='c'):
    return a + b + num_opcional

print(suma(b='a', a='b'))

