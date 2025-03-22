import msvcrt
import time
import sys
import os
import graphlib
class Nodo:
    def __init__ (self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ABB:
    def __init__ (self):
        self.Raiz = None
        self.valores_ingresados = set()
    
    def agregarArchivo(self, valor, nodo):
        if nodo == None:
            return Nodo(valor)
        if nodo.valor < valor:
            nodo.derecha = self.agregarArchivo(valor, nodo.derecha)
        elif nodo.valor > valor:
            nodo.izquierda = self.agregarArchivo(valor, nodo.izquierda)
        return nodo

    def agregar(self, valor, nodo):
        if nodo == None:
            return Nodo(valor)
        if nodo.valor == valor:
            return print("Valor duplicado no se puede ingresar un nodo con un valor ya existente: ",valor,"\n No se inserto")
        if nodo.valor < valor:
            nodo.derecha = self.agregar(valor, nodo.derecha)
        elif nodo.valor > valor:
            nodo.izquierda = self.agregar(valor, nodo.izquierda)
        print("Se inserto el nodo con el valor ingresado: ",valor)
        return nodo

    def inOrder(self, nodo):
        if nodo != None:
            self.inOrder(nodo.izquierda)
            print (nodo.valor)
            self.inOrder(nodo.derecha)

    def preOrder(self, nodo):
        if nodo != None:
            print (nodo.valor)
            self.preOrder(nodo.izquierda)
            self.preOrder(nodo.derecha)
    
    def postOrder(self, nodo):
        if nodo != None:
            self.postOrder(nodo.izquierda)
            self.postOrder(nodo.derecha)
            print (nodo.valor)

    def buscar(self, valor, nodo):
        if nodo is None:
            return print("No se encontre el nodo con el valor ingresado")
        if nodo.valor == valor:
            return print("Se encontro el nodo con el valor ingresado: ",valor)
        if valor < nodo.valor:
            return self.buscar(valor, nodo.izquierda)
        else:
            return self.buscar(valor, nodo.derecha)

    def encontrar_minimo(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    def eliminar(self, valor, nodo):
        if nodo is None:
            print("No existe un nodo con el valor ingresado.")
            return nodo
        if valor < nodo.valor:
            nodo.izquierda = self.eliminar(valor, nodo.izquierda)
        elif valor > nodo.valor:
            nodo.derecha = self.eliminar(valor, nodo.derecha)
        else:
            print("Se realizo la eliminarcion del nodo con el valor de: ",valor)
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            sucesor = self.encontrar_minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self.eliminar(sucesor.valor, nodo.derecha)
        return nodo

    def leerTXT(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r") as archivo:
                mensajes = ["Cargando   ", "Cargando.  ", "Cargando.. ", "Cargando..."]

                contenido = archivo.read().strip()
                valores = map(int, contenido.split(","))
                for valor in valores:
                    if valor in self.valores_ingresados:
                        print("Valor duplicado (",valor,") no se inserto")
                    else:
                        self.Raiz = self.agregarArchivo(valor, self.Raiz)
                        self.valores_ingresados.add(valor)
                        for mensaje in mensajes:
                            sys.stdout.write("\r" + mensaje)
                            sys.stdout.flush()
                            time.sleep(0.5)
        except FileNotFoundError:
            print("Error: No se encontró el archivo en: ",nombre_archivo)
        except ValueError:
            print("Error: El archivo contiene datos no válidos. Asegúrate de que sean números separados por comas.")
    
    def graficar(self):
        if self.Raiz is None:
            print("⚠️  El árbol está vacío, no se puede graficar.")
            return
        
        dot = graphviz.Digraph(comment="Árbol Binario de Búsqueda")

        def agregar_nodos(nodo):
            if nodo is not None:
                dot.node(str(nodo.valor), str(nodo.valor))  # Crear nodo
                if nodo.izquierda:
                    dot.edge(str(nodo.valor), str(nodo.izquierda.valor))  # Conectar izquierda
                    agregar_nodos(nodo.izquierda)
                if nodo.derecha:
                    dot.edge(str(nodo.valor), str(nodo.derecha.valor))  # Conectar derecha
                    agregar_nodos(nodo.derecha)

        agregar_nodos(self.Raiz)

        dot.render("ABB", format="png", cleanup=True)  # Guardar como imagen
        print("✅  Se ha generado el árbol en 'ABB.png'")

Arbol = ABB()
#C:/Users/agust/Desktop/Clases/SEMESTRE5/PROGRAMACION III/Python/Tarea3/datosArbol.txt

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("|--------------------------------------------------|")
    print("|         ARBOL BINARIO DE BUSQUEDA (ABB)          |")
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
    print("8) Generar Arbol ABB con Graphviz")
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
            print("Accion Finalizada")
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
        elif n==8:
            os.system('cls' if os.name == 'nt' else 'clear')
            Arbol.graficar()
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