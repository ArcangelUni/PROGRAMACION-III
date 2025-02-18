import msvcrt
def convertir_a_binario(numero):
    if numero == 0:
        return "0"
    if numero == 1:
        return "1"
    return convertir_a_binario(numero//2)+str(numero%2)

#print(convertir_a_binario(7))

def contar_digitos(numero):
    if numero==0:
        return 0
    
    return 1+contar_digitos(numero//10)

#print(contar_digitos(7654321))

def raiz_cuadrada_entera(numero):
    if numero<0:
        return "No se puede calcular la raiz cuadrada de un numero negativo"
    return calcular_raiz_cuadrada(numero,0)

def calcular_raiz_cuadrada(numero, x):
    if x*x>numero:
        return x-1
    return calcular_raiz_cuadrada(numero,x+1)

#print(raiz_cuadrada_entera(10))

def valor_romano(numero):
    valores={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    return valores.get(numero,0)

def convertir_a_decimal(numero_romano,indice=0):
    if indice == len(numero_romano)-1:
        return valor_romano(numero_romano[indice])
    
    actual = valor_romano(numero_romano[indice])
    siguiente = valor_romano(numero_romano[indice+1])

    if actual<siguiente:
        return -actual + convertir_a_decimal(numero_romano, indice + 1)
    else:
        return actual + convertir_a_decimal(numero_romano, indice + 1)

#print(convertir_a_decimal("XX"))

def suma_numeros_enteros(numero):
    if numero==0:
        return 0
    return numero+suma_numeros_enteros(numero-1)

#print(suma_numeros_enteros(10))

while True:
    print()
    print("|--------------------------------------------------|")
    print("|                   RECURSIVIDAD                   |")
    print("|--------------------------------------------------|")
    print()
    print("¿Que quieres realizar?")
    print("1) Convertir a Binario")
    print("2) Contar Digitos")
    print("3) Raiz Cuadrada Entera")
    print("4) Convertir a Decimal desde Romano")
    print("5) Suma de Numeros Enteros")
    print("0) Salir")
    print()

    try:
        n=int(input("Ingresa la opcion: "))

        if n==1:
            print()
            print("---------------------------------")
            dato=int(input("Ingresa un Entero: "))
            print(f"El numero {dato} a Binario es: {convertir_a_binario(dato)}")
            print("---------------------------------")
        elif n==2:
            print()
            print("---------------------------------")
            dato=int(input("Ingresa un valor entero: "))
            print(f"El numero {dato} tiene la cantidad de: {contar_digitos(dato)} digitos")
            print("---------------------------------")
        elif n==3:
            print()
            print("---------------------------------")
            dato=int(input("Ingresa un numero entero: "))
            print(f"La raiz cuadrada de {dato} es: {raiz_cuadrada_entera(dato)}")
            print("---------------------------------")
        elif n==4:
            print()
            print("---------------------------------")
            dato=str(input("Ingresa un numero romano(Mayusculas): "))
            print(f"El numero romano {dato} es a Decimal: {convertir_a_decimal(dato)}")
            print("---------------------------------")
        elif n==5:
            print()
            print("---------------------------------")
            dato=int(input("Ingresa un Entero: "))
            print(f"La suma desde 0 hasta {dato} es : {suma_numeros_enteros(dato)}")
            print("---------------------------------")
        elif n==0:
            break
        print()
        print("Presione una tecla para continuar...")
        msvcrt.getch()
    except:
        print()
        print("Ingrese un numero del menu")
        print("Presione una tecla para continuar...")
        msvcrt.getch()