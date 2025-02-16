import msvcrt
class nodo:
    def __init__ (self,nombre):
        self.nombre = nombre
        self.siguiente = None
        self.anterior = None

class lista:
    def __init__(self):
        self.inicio = None
        self.final = None
        self.size = 0

    def insertar_inicio(self, nombre):

        if self.size!=0:
            nuevo_nodo = nodo(nombre)
            nuevo_nodo.siguiente = self.inicio
            self.inicio.anterior=nuevo_nodo
            self.inicio = nuevo_nodo
            self.inicio.anterior=None

        else:
            nuevo_nodo = nodo(nombre)
            nuevo_nodo.siguiente = self.inicio
            nuevo_nodo.anterior = None
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo

        self.size+=1
    
    def insertar_final(self, nombre):
        if self.size!=0:
            nuevo_nodo = nodo(nombre)
            nuevo_nodo.anterior = self.final
            self.final.siguiente = nuevo_nodo
            self.final=nuevo_nodo
            self.final.siguiente=None
        else:
            nuevo_nodo = nodo(nombre)
            nuevo_nodo.siguiente = self.inicio
            nuevo_nodo.anterior = None
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo

    def eliminar_inicio(self):
        if self.size!=0:
            if self.inicio.siguiente==None and self.inicio.anterior==None:
                self.inicio=None
                self.final=None
            else:
                self.inicio=self.inicio.siguiente
                self.inicio.anterior=None
            self.size-=1
        else:
            print("La lista esta vacia")

    def eliminar_final(self):
        if self.size!=0:
            if self.final.siguiente==None and self.final.anterior==None:
                self.inicio=None
                self.final=None
            else:
                self.final = self.final.anterior
                self.final.siguiente=None
            self.size-=1
        else:
            print("La lista esta vacia")

    def eliminar_por_valor(self,nombre):
        temp = self.inicio
        while temp:
            if temp.nombre == nombre:
                if temp.anterior:
                    temp.anterior.siguiente = temp.siguiente
                else:
                    self.inicio = temp.siguiente
                
                if temp.siguiente:
                    temp.siguiente.anterior = temp.anterior
                else:
                    self.final = temp.anterior
            temp = temp.siguiente

    def listar_inicio(self):
        temp = self.inicio
        while temp != None:
            print(temp.nombre+"->")
            temp = temp.siguiente

    def listar_final(self):
        temp = self.final
        while temp != None:
            print(temp.nombre+"->")
            temp = temp.anterior


estudiante = lista()

def InsertInicio():
    try:
        print("---------------------------------")
        datN=str(input("Ingresa el Nombre: "))
        estudiante.insertar_inicio(datN)
        print("---------------------------------")
    except:
        print()
        print("Por favor ingrese caracteres correctos")
        print("Presione una tecla para continuar...")
        msvcrt.getch()

def InsertFinal():
    try:
        print("---------------------------------")
        datN=str(input("Ingresa el Nombre: "))
        estudiante.insertar_final(datN)
        print("---------------------------------")
    except:
        print()
        print("Por favor ingrese caracteres correctos")
        print("Presione una tecla para continuar...")
        msvcrt.getch()

def DeleteNodoValor():
    try:
        print("---------------------------------")
        datN=str(input("Ingresa el Nombre: "))
        estudiante.eliminar_por_valor(datN)
        print("---------------------------------")
    except:
        print()
        print("Por favor ingrese caracteres correctos")
        print("Presione una tecla para continuar...")
        msvcrt.getch()

while True:
    print()
    print("|--------------------------------------------------|")
    print("|            LISTA DOBLEMENTE ENLAZADA             |")
    print("|--------------------------------------------------|")
    print()
    print("¿Que quieres realizar?")
    print("1) Insertar al Inicio")
    print("2) Insertar al Final")
    print("3) Eliminar Primer Nodo")
    print("4) Eliminar Ultimo Nodo")
    print("5) Eliminar Nodo por Valor")
    print("6) Imprimir de Inicio a Final")
    print("7) Imprimir de Final a Inicio")
    print("0) Salir")
    print()

    try:
        n=int(input("Ingresa la opcion: "))

        if n==1:
            InsertInicio()
        elif n==2:
            InsertFinal()
        elif n==3:
            print()
            print("---------------------------------")
            estudiante.eliminar_inicio()
            print("---------------------------------")
        elif n==4:
            print()
            print()
            print("---------------------------------")
            estudiante.eliminar_final()
            print("---------------------------------")
        elif n==5:
            print()
            print("---------------------------------")
            DeleteNodoValor()
            print("---------------------------------")
        elif n==6:
            print()
            print("---------------------------------")
            estudiante.listar_inicio()
            print("---------------------------------")
        elif n==7:
            print()
            print("---------------------------------")
            estudiante.listar_final()
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



#print("Insertando al Inicio")
#estudiante.insertar_inicio("Angel")
#estudiante.insertar_inicio("Wendy")
#estudiante.insertar_inicio("Nancy")

#print("LISTANDO INICIO")
#estudiante.listar_inicio()
#print("LISTANDO FINAL")
#estudiante.listar_final()


#print("Insertando al Final")
#estudiante.insertar_final("Roberto")
#estudiante.insertar_final("Astrid")
#estudiante.insertar_final("Agustin")

#print("LISTANDO INICIO")
#estudiante.listar_inicio()
#print("LISTANDO FINAL")
#estudiante.listar_final()

#print("Eliminando un nodo")
#estudiante.eliminar_por_valor("Roberto")

#print("LISTANDO INICIO")
#estudiante.listar_inicio()
#print("LISTANDO FINAL")
#estudiante.listar_final()

#print("Eliminando el primer nodo")
#estudiante.eliminar_inicio()
#print("LISTANDO INICIO")
#estudiante.listar_inicio()
#print("LISTANDO FINAL")
#estudiante.listar_final()

#print("Eliminando el ultimo nodo")
#estudiante.eliminar_final()
#print("LISTANDO INICIO")
#estudiante.listar_inicio()
#print("LISTANDO FINAL")
#estudiante.listar_final()
