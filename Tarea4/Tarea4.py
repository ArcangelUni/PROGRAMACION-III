import msvcrt
import time
import sys
import os

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    def __init__(self):
        self.Raiz = None
        self.valores_ingresados = set()
    
    def agregarArchivo(self, valor, nodo):
        if not nodo:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self.agregarArchivo(valor, nodo.izquierda)
        else:
            nodo.derecha = self.agregarArchivo(valor, nodo.derecha)

        self.actualizar_altura(nodo)
        return self.balancear_nodo(nodo)

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotacion_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        self.actualizar_altura(y)
        self.actualizar_altura(x)

        return x

    def rotacion_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        self.actualizar_altura(x)
        self.actualizar_altura(y)

        return y

    def balancear_nodo(self, nodo):
        balance = self.obtener_balance(nodo)

        if balance > 1:
            if self.obtener_balance(nodo.izquierda) < 0:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
            return self.rotacion_derecha(nodo)

        if balance < -1:
            if self.obtener_balance(nodo.derecha) > 0:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
            return self.rotacion_izquierda(nodo)

        return nodo

    def agregar(self, valor, nodo):
        if not nodo:
            print("Se inserto el nodo con el valor ingresado:", valor)
            return Nodo(valor)

        if valor == nodo.valor:
            print("Valor duplicado no se puede ingresar un nodo con un valor ya existente:", valor, "\n No se inserto")
            return nodo
        elif valor < nodo.valor:
            nodo.izquierda = self.agregar(valor, nodo.izquierda)
        else:
            nodo.derecha = self.agregar(valor, nodo.derecha)

        self.actualizar_altura(nodo)
        return self.balancear_nodo(nodo)

    def inOrder(self, nodo):
        if nodo:
            self.inOrder(nodo.izquierda)
            print(nodo.valor)
            self.inOrder(nodo.derecha)

    def preOrder(self, nodo):
        if nodo:
            print(nodo.valor)
            self.preOrder(nodo.izquierda)
            self.preOrder(nodo.derecha)

    def postOrder(self, nodo):
        if nodo:
            self.postOrder(nodo.izquierda)
            self.postOrder(nodo.derecha)
            print(nodo.valor)

    def buscar(self, valor, nodo, nivel=0):
        if not nodo:
            print("No se encontró el nodo con el valor ingresado")
            return
        if valor == nodo.valor:
            print(f"Se encontró el nodo con el valor ingresado: ",valor," en la altura del árbol: ",nivel)
            return
        elif valor < nodo.valor:
            return self.buscar(valor, nodo.izquierda, nivel + 1)
        else:
            return self.buscar(valor, nodo.derecha, nivel + 1)


    def encontrar_minimo(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    def eliminar(self, valor, nodo):
        if not nodo:
            print("No existe un nodo con el valor ingresado.")
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self.eliminar(valor, nodo.izquierda)
        elif valor > nodo.valor:
            nodo.derecha = self.eliminar(valor, nodo.derecha)
        else:
            print("Se realizó la eliminación del nodo con el valor de:", valor)
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda
            temp = self.encontrar_minimo(nodo.derecha)
            nodo.valor = temp.valor
            nodo.derecha = self.eliminar(temp.valor, nodo.derecha)

        self.actualizar_altura(nodo)
        return self.balancear_nodo(nodo)

    def leerTXT(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r") as archivo:
                mensajes = ["Cargando   ", "Cargando.  ", "Cargando.. ", "Cargando..."]

                contenido = archivo.read().strip()
                valores = map(int, contenido.split(","))
                for valor in valores:
                    if valor in self.valores_ingresados:
                        print("Valor duplicado (", valor, ") no se insertó")
                    else:
                        self.Raiz = self.agregarArchivo(valor, self.Raiz)
                        self.valores_ingresados.add(valor)
                        for mensaje in mensajes:
                            sys.stdout.write("\r" + mensaje)
                            sys.stdout.flush()
                            time.sleep(0.5)
        except FileNotFoundError:
            print("Error: No se encontró el archivo en:", nombre_archivo)
        except ValueError:
            print("Error: El archivo contiene datos no válidos. Asegúrate de que sean números separados por comas.")

Arbol = AVL()
#C:/Users/agust/Desktop/Clases/SEMESTRE5/PROGRAMACION III/Python/Tarea4/datosArbolAVL.txt

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("|--------------------------------------------------|")
    print("|                   ARBOL AVL                      |")
    print("|--------------------------------------------------|")
    print()
    print("¿Que quieres realizar?")
    print("1) Cargar archivo .txt")
    print("2) Insertar")
    print("3) Buscar")
    print("4) Eliminar")
    print("5) Recorrido inOrder")
    print("6) Recorrido preOrder")
    print("7) Recorrido postOrder")
    print("0) Salir")
    print()

    try:
        n=int(input("Ingresa la opcion: "))
        if n==1:
            os.system('cls' if os.name == 'nt' else 'clear')
            txt=str(input("Ingrese la direccion del archivo .txt: "))
            Arbol.leerTXT(txt)
            sys.stdout.write("\r ¡Carga completada! \n")
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch() 
        elif n==2:
            os.system('cls' if os.name == 'nt' else 'clear')
            data=int(input("Ingresa el valor: "))
            Arbol.Raiz = Arbol.agregar(data, Arbol.Raiz)
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
        elif n==3:
            os.system('cls' if os.name == 'nt' else 'clear')
            data=int(input("Ingresa el valor del nodo a buscar: "))
            Arbol.buscar(data, Arbol.Raiz)
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
        elif n==4:
            os.system('cls' if os.name == 'nt' else 'clear')
            data=int(input("Ingresa el valor del nodo a eliminar: "))
            Arbol.Raiz = Arbol.eliminar(data, Arbol.Raiz)
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
        elif n==5:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Imprimiendo recorrido inOrder")
            Arbol.inOrder(Arbol.Raiz)
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
        elif n==6:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Imprimiendo recorrido preOrder")
            Arbol.preOrder(Arbol.Raiz)
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
        elif n==7:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Imprimiendo recorrido postOrder")
            Arbol.postOrder(Arbol.Raiz)
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
        elif n==0:
            print()
            print("Presione cualquier tecla para salir...")
            msvcrt.getch()
            os.system("cls" if os.name == "nt" else "clear")
            break
        else:
            print()
            print("Ingrese un numero del menu")
            print("Presione cualquier tecla para continuar...")
            msvcrt.getch()
    except:
        print()
        print("Ingrese un numero del menu")
        print("Presione cualquier tecla para continuar...")
        msvcrt.getch()