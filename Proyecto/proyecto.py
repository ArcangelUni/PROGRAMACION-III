from math import radians, sin, cos, sqrt, atan2
import folium
from graphviz import Digraph
import csv
import csv

class NodoB:
    def __init__(self, es_hoja=True):
        self.claves = []    # Claves almacenadas en el nodo
        self.hijos = []     # Referencias a hijos (si no es hoja)
        self.es_hoja = es_hoja

class Hospedaje:
    def __init__(self, id, nombre, tipo, ubicacion, precio, calificacion, estadia, comentarios=""):
        self.id = int(id)
        self.nombre = nombre
        self.tipo = tipo
        self.precio = float(precio)
        self.ubicacion = ubicacion
        self.calificacion = float(calificacion)
        self.estadia = float(estadia)
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
    def __init__(self, id, nombre, tipo, ubicacion, precio, calificacion, estadia, comentarios=""):
        self.id = int(id)
        self.nombre = nombre
        self.tipo = tipo
        self.precio = float(precio)
        self.ubicacion = ubicacion
        self.calificacion = float(calificacion)
        self.estadia = float(estadia)
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
                estadia = float(fila["Estadia"])
                comentarios = fila["Comentarios"]

                if entidad.lower() == "hospedaje":
                    hospedaje = Hospedaje(id, nombre, entidad, f"{latitud}, {longitud}", precio, calificacion, estadia, comentarios)
                    arbol_hospedajes.insertar(hospedaje)
                else:
                    lugar = LugarTuristico(id, nombre, entidad, f"{latitud}, {longitud}", precio, calificacion, estadia, comentarios)
                    arbol_turisticos.insertar(lugar)
            except KeyError as e:
                print(f"Columna faltante: {e}")
            except ValueError as e:
                print(f"Error de conversión: {e}")
    return arbol_hospedajes, arbol_turisticos

# Clase para nodos del grafo (lugares turísticos)
class Lugar:
    def __init__(self, id, nombre, lat, lon, precio, calificacion, tiempo_estadia):
        self.id = id
        self.nombre = nombre
        self.lat = lat
        self.lon = lon
        self.precio = precio
        self.calificacion = calificacion
        self.tiempo_estadia = tiempo_estadia

# Clase para el grafo ponderado
class Grafo:
    def __init__(self):
        self.vertices = []

    def agregar_vertice(self, lugar):
        self.vertices.append(lugar)

    def calcular_distancia(self, lugar1, lugar2):
        R = 6371  # Radio de la Tierra en km
        lat1 = radians(lugar1.lat)
        lon1 = radians(lugar1.lon)
        lat2 = radians(lugar2.lat)
        lon2 = radians(lugar2.lon)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c  # distancia en km

# ========== ALGORITMO DE RUTA RECOMENDADA ==========

def construir_grafo(lugares):
    grafo = Grafo()
    for lugar in lugares:
        grafo.agregar_vertice(lugar)
    return grafo

def recomendar_ruta(grafo, origen_coord, presupuesto_diario, tiempo_maximo=8):
    origen_lugar = Lugar(-1, "Origen", origen_coord[0], origen_coord[1], 0, 0, 0)
    candidatos = []

    for lugar in grafo.vertices:
        distancia = grafo.calcular_distancia(origen_lugar, lugar)
        tiempo_traslado = distancia / 50  # 50 km/h promedio
        tiempo_total = tiempo_traslado + lugar.tiempo_estadia
        puntaje = lugar.calificacion / (distancia + 1)
        candidatos.append((puntaje, tiempo_traslado, lugar))

    candidatos.sort(reverse=True)

    ruta_recomendada = []
    tiempos_traslado = []
    tiempo_acumulado = 0
    presupuesto_acumulado = 0
    origen_actual = origen_lugar

    for _, _, lugar in candidatos:
        distancia = grafo.calcular_distancia(origen_actual, lugar)
        tiempo_traslado = distancia / 50
        tiempo_lugar = tiempo_traslado + lugar.tiempo_estadia
        nuevo_tiempo_total = tiempo_acumulado + tiempo_lugar
        nuevo_presupuesto_total = presupuesto_acumulado + lugar.precio

        if nuevo_tiempo_total <= tiempo_maximo and nuevo_presupuesto_total <= presupuesto_diario:
            ruta_recomendada.append(lugar)
            tiempos_traslado.append(tiempo_traslado)
            tiempo_acumulado = nuevo_tiempo_total
            presupuesto_acumulado = nuevo_presupuesto_total
            origen_actual = lugar

    return ruta_recomendada, tiempos_traslado

def mostrar_en_mapa(origen_coord, lugares):
    mapa = folium.Map(location=origen_coord, zoom_start=13)
    folium.Marker(location=origen_coord, popup="Origen", icon=folium.Icon(color="blue")).add_to(mapa)
    for lugar in lugares:
        folium.Marker(
            location=(lugar.lat, lugar.lon),
            popup=f"{lugar.nombre}\nCalificación: {lugar.calificacion}\nPrecio: Q{lugar.precio}",
            icon=folium.Icon(color="green")
        ).add_to(mapa)
    puntos = [origen_coord] + [(l.lat, l.lon) for l in lugares]
    folium.PolyLine(puntos, color="red", weight=2.5).add_to(mapa)
    mapa.save("static/ruta_recomendada.html")

# ========== CONVERSIÓN DESDE ÁRBOL B ==========

def convertir_arbol_a_lugares(arbol_turisticos):
    lugares = []

    def recorrer_nodo(nodo):
        for clave in nodo.claves:
            lat, lon = map(float, clave.ubicacion.split(","))
            lugar = Lugar(
                id=clave.id,
                nombre=clave.nombre,
                lat=lat,
                lon=lon,
                precio=float(clave.precio),
                calificacion=clave.calificacion,
                tiempo_estadia=clave.estadia
            )
            lugares.append(lugar)
        for hijo in nodo.hijos:
            recorrer_nodo(hijo)

    recorrer_nodo(arbol_turisticos.raiz)
    return lugares

def insertar_claves(nodo, arbol_destino):
    for clave in nodo.claves:
        arbol_destino.insertar(clave)
    for hijo in nodo.hijos:
        insertar_claves(hijo, arbol_destino)

def insertar_claves_arbol_en_otro(origen, destino):
    def recorrer_e_insertar(nodo):
        if nodo is None:
            return
        for clave in nodo.claves:
            destino.insertar(clave)
        for hijo in nodo.hijos:
            recorrer_e_insertar(hijo)

    recorrer_e_insertar(origen.raiz)

def exportar_ruta_csv(ruta, tiempos_traslado, ruta_archivo="ruta_recomendada.csv"):
    with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Nombre", "Precio", "Calificación", "Tiempo Estadia", "Tiempo Traslado (desde anterior)"])
        
        for i, lugar in enumerate(ruta):
            traslado = tiempos_traslado[i-1] if i > 0 else 0
            escritor.writerow([lugar.nombre, lugar.precio, lugar.calificacion, lugar.tiempo_estadia, round(traslado, 2)])
