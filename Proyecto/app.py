from flask import Flask, request, render_template, redirect
from proyecto import *
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

arbol_hospedajes = ArbolB(G=5)
arbol_turisticos = ArbolB(G=5)
lugares_turisticos = []
grafo = Grafo()

@app.route('/')
def index():
    return render_template('index.html', ruta_generada=False)

@app.route('/procesar', methods=['POST'])
def procesar():
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])
    presupuesto = float(request.form['presupuesto'])

    ruta, tiempos_traslado = recomendar_ruta(grafo, (lat, lon), presupuesto)
    mostrar_en_mapa((lat, lon), ruta)

    exportar_ruta_csv(ruta, tiempos_traslado, ruta_archivo="static/ruta_recomendada.csv")

    return render_template('index.html', ruta_generada=True, ruta=ruta, tiempos_traslado=tiempos_traslado)


@app.route("/cargar_csv", methods=["POST"])
def cargar_csv():
    global arbol_hospedajes, arbol_turisticos, lugares_turisticos, grafo

    archivo = request.files["archivo"]
    if archivo.filename.endswith(".csv"):
        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)
        
        nuevos_hospedajes, nuevos_turisticos = cargar_datos_desde_csv(ruta)

        insertar_claves(nuevos_hospedajes.raiz, arbol_hospedajes)
        insertar_claves(nuevos_turisticos.raiz, arbol_turisticos)

        arbol_turisticos.exportar_graphviz().render("Turistico", format="jpg", cleanup=True)
        arbol_hospedajes.exportar_graphviz().render("Hospedaje", format="jpg", cleanup=True)

        lugares_turisticos = convertir_arbol_a_lugares(arbol_turisticos)
        grafo = construir_grafo(lugares_turisticos)

        return render_template("index.html", mensaje="Archivo CSV cargado correctamente", ruta_generada=False)
    else:
        return render_template("index.html", mensaje="Error: Solo se aceptan archivos CSV.", ruta_generada=False)

@app.route("/agregar_manual", methods=["POST"])
def agregar_manual():
    global arbol_hospedajes, arbol_turisticos, lugares_turisticos, grafo

    tipo = request.form["tipo"]
    id = int(request.form["id"])
    nombre = request.form["nombre"]
    lat = float(request.form["lat"])
    lon = float(request.form["lon"])
    precio = float(request.form["precio"])
    calificacion = float(request.form["calificacion"])
    estadia = float(request.form["estadia"])
    comentarios = request.form.get("comentarios", "")
    ubicacion = f"{lat}, {lon}"

    if tipo == "hospedaje":
        hospedaje = Hospedaje(id, nombre, tipo, ubicacion, precio, calificacion, estadia, comentarios)
        arbol_hospedajes.insertar(hospedaje)
        arbol_hospedajes.exportar_graphviz().render("Hospedaje", format="jpg", cleanup=True)
    else:
        lugar = LugarTuristico(id, nombre, tipo, ubicacion, precio, calificacion, estadia, comentarios)
        arbol_turisticos.insertar(lugar)
        arbol_turisticos.exportar_graphviz().render("Turistico", format="jpg", cleanup=True)

        # También actualizar el grafo si se agregó un nuevo lugar turístico
        lugar_convertido = Lugar(id, nombre, lat, lon, precio, calificacion, estadia)
        grafo.agregar_vertice(lugar_convertido)

    return render_template("index.html", mensaje="Elemento agregado correctamente.", ruta_generada=False)

if __name__ == '__main__':
    app.run(debug=True)
