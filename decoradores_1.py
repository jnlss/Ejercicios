#Ejercicio 1: comprobación de argumentos positivos
#Crea un decorador @validate_arguments que compruebe que todos los argumentos pasados a una función son enteros positivos. En caso contrario, debe saltar la excepción ValueError.

def validate_arguments(función_genérica):
    
    def wrapper(*args, **kwargs):
        for argumento in args:
            assert type(argumento) == int and argumento > 0, ValueError
            
        for value in kwargs.values():
            assert type(argumento) == int and value > 0, ValueError
        
        return función_genérica(*args, **kwargs)
    
    return wrapper



@validate_arguments
def suma(a, b, num_opcional=1):
    return a + b + num_opcional

print(suma(b='a', a='b'))

