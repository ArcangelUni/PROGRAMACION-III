'''from collections import deque
from graphviz import Digraph

class NodoB:
    def __init__(self, es_hoja=True):
        self.claves = []
        self.hijos = []
        self.es_hoja = es_hoja

class ArbolB:
    def __init__(self, G):
        self.raiz = NodoB(True)
        self.G = G
        self.max_claves = G - 1
        self.min_claves = ((1 + G) // 2) - 1
        self.contador_grafos = 0  # Para generar nombres únicos

    def insertar(self, clave):
        raiz = self.raiz
        if len(raiz.claves) == self.max_claves:
            nueva_raiz = NodoB(False)
            nueva_raiz.hijos.append(raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self._insertar_no_lleno(nueva_raiz, clave)
            self.raiz = nueva_raiz
        else:
            self._insertar_no_lleno(raiz, clave)
        # Visualizar el árbol después de insertar esta clave
        self.generar_grafico(clave)

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1
        if nodo.es_hoja:
            nodo.claves.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == self.max_claves:
                self._dividir_hijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave)

    def _dividir_hijo(self, padre, i):
        G = self.G
        nodo_lleno = padre.hijos[i]
        nuevo_nodo = NodoB(nodo_lleno.es_hoja)
        medio = G // 2 - 1
        #medio = G // 2
        clave_medio = nodo_lleno.claves[medio]

        nuevo_nodo.claves = nodo_lleno.claves[medio + 1:]
        nodo_lleno.claves = nodo_lleno.claves[:medio]

        if not nodo_lleno.es_hoja:
            nuevo_nodo.hijos = nodo_lleno.hijos[medio + 1:]
            nodo_lleno.hijos = nodo_lleno.hijos[:medio + 1]

        padre.hijos.insert(i + 1, nuevo_nodo)
        padre.claves.insert(i, clave_medio)

    def generar_grafico(self, clave):
        dot = Digraph(comment=f'Arbol B - Insertando {clave}')
        self._crear_nodos(dot, self.raiz)
        self._crear_aristas(dot, self.raiz)
        nombre_archivo = f'arbol_b_insert_{self.contador_grafos:02d}_{clave}'
        dot.render(nombre_archivo, format='png', cleanup=True)
        print(f'Generado: {nombre_archivo}.png')
        self.contador_grafos += 1

    def _crear_nodos(self, dot, nodo, id_padre=None, id_actual=[0]):
        id_nodo = f'n{id_actual[0]}'
        etiqueta = '|'.join(str(c) for c in nodo.claves)
        dot.node(id_nodo, f'<f0> {etiqueta}', shape='record')
        nodo._id = id_nodo
        id_actual[0] += 1
        for hijo in nodo.hijos:
            self._crear_nodos(dot, hijo, id_nodo, id_actual)

    def _crear_aristas(self, dot, nodo):
        for i, hijo in enumerate(nodo.hijos):
            dot.edge(nodo._id, hijo._id)
            self._crear_aristas(dot, hijo)

arbol = ArbolB(G=4)
for clave in [100,15,55,13,101,65,38,99,105]:
    arbol.insertar(clave)'''

from graphviz import Digraph
import csv

# Nodo del Árbol B
class NodoB:
    def __init__(self, es_hoja=True):
        self.claves = []    # Claves almacenadas en el nodo
        self.hijos = []     # Referencias a hijos (si no es hoja)
        self.es_hoja = es_hoja

class Hospedaje:
    def __init__(self, id, nombre, tipo, ubicacion, precio, calificacion, comentarios=""):
        self.id = int(id)
        self.nombre = nombre
        self.tipo = tipo
        self.precio = float(precio)
        self.ubicacion = ubicacion
        self.calificacion = float(calificacion)
        self.comentarios = comentarios

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return (f" {self.id} | {self.nombre} ({self.tipo})\n"
                f"{self.ubicacion} | Q {self.precio} | ⭐ {self.calificacion}/5\n"
                f"{self.comentarios}")


class LugarTuristico:
    def __init__(self, id, nombre, tipo, ubicacion, precio, calificacion, comentarios=""):
        self.id = int(id)
        self.nombre = nombre
        self.tipo = tipo
        self.precio = float(precio)
        self.ubicacion = ubicacion
        self.calificacion = float(calificacion)
        self.comentarios = comentarios

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return (f" {self.id} |{self.nombre} ({self.tipo})\n"
                f"{self.ubicacion} | Q {self.precio} | ⭐ {self.calificacion}/5\n"
                f"{self.comentarios}")


# Árbol B genérico
class ArbolB:
    def __init__(self, G):
        self.raiz = NodoB(True)
        self.G = G
        self.max_claves = G - 1
        self.min_claves = ((1 + G) // 2) - 1

    def insertar(self, clave):
        raiz = self.raiz
        if len(raiz.claves) == self.max_claves:
            nueva_raiz = NodoB(False)
            nueva_raiz.hijos.append(raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self._insertar_no_lleno(nueva_raiz, clave)
            self.raiz = nueva_raiz
        else:
            self._insertar_no_lleno(raiz, clave)

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1
        if nodo.es_hoja:
            nodo.claves.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == self.max_claves:
                self._dividir_hijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave)

    def _dividir_hijo(self, padre, i):
        G = self.G
        nodo_lleno = padre.hijos[i]
        nuevo_nodo = NodoB(nodo_lleno.es_hoja)

        medio = G // 2  # Promover la clave central
        clave_medio = nodo_lleno.claves[medio]

        nuevo_nodo.claves = nodo_lleno.claves[medio + 1:]
        nodo_lleno.claves = nodo_lleno.claves[:medio]

        if not nodo_lleno.es_hoja:
            nuevo_nodo.hijos = nodo_lleno.hijos[medio + 1:]
            nodo_lleno.hijos = nodo_lleno.hijos[:medio + 1]

        padre.hijos.insert(i + 1, nuevo_nodo)
        padre.claves.insert(i, clave_medio)

    def exportar_graphviz(self):
        dot = Digraph()
        self._exportar_nodo(self.raiz, dot)
        return dot

    def _exportar_nodo(self, nodo, dot, contador=[0]):
        indice = contador[0]
        contador[0] += 1
        clave_str = "|".join(str(c) for c in nodo.claves)
        nombre_nodo = f"n{indice}"
        dot.node(nombre_nodo, f"<f0> {clave_str}", shape="record")
        if not nodo.es_hoja:
            for i, hijo in enumerate(nodo.hijos):
                hijo_nombre = self._exportar_nodo(hijo, dot, contador)
                dot.edge(nombre_nodo, hijo_nombre)
        return nombre_nodo

def cargar_datos_desde_csv(ruta):
    arbol_hospedajes = ArbolB(G=5)
    arbol_turisticos = ArbolB(G=5)

    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            try:
                id = int(fila['Id'])
                nombre = fila["Nombre"]
                entidad = fila["Entidad"]
                latitud = float(fila["Latitud"])
                longitud = float(fila["Longitud"])
                precio = float(fila["Precio"])
                calificacion = float(fila["Calificacion"])
                comentarios = fila["Comentarios"]

                if entidad.lower() == "hospedaje":
                    hospedaje = Hospedaje(id, nombre, entidad, f"{latitud}, {longitud}", precio, calificacion, comentarios)
                    arbol_hospedajes.insertar(hospedaje)
                else:
                    lugar = LugarTuristico(id, nombre, entidad, f"{latitud}, {longitud}", precio, calificacion, comentarios)
                    arbol_turisticos.insertar(lugar)
            except KeyError as e:
                print(f"Columna faltante: {e}")
            except ValueError as e:
                print(f"Error de conversión: {e}")
    return arbol_hospedajes, arbol_turisticos

# Cargar desde el CSV
arbol_hospedajes, arbol_turisticos = cargar_datos_desde_csv("datos.csv")

# Generar los archivos de Graphviz
arbol_turisticos.exportar_graphviz().render("Turistico", format="jpg", cleanup=True)
arbol_hospedajes.exportar_graphviz().render("Hospedaje", format="jpg", cleanup=True)