from flask import Flask, redirect, url_for, render_template, request
from grammar import parse
import base64
import graphviz
app = Flask(__name__)

tmp_val=''
parsed_tree = None


@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')


@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"];
        global tmp_val
        tmp_val=inpt
        return redirect(url_for("output"))
    else:
        f = open("./entrada.txt", "r")
        entrada = f.read()
        return render_template('analyze.html', initial=entrada)

@app.route('/output')
def output():
    global tmp_val
    global parsed_tree
    result = parse(tmp_val)
    parsed_tree = result
    return render_template('output.html', input=result)

@app.route("/reporte")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def reporte():
    return render_template('reporte.html')

@app.route("/tree")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def tree():
    global parsed_tree
    archivo_dot = parsed_tree.empiezoArbol()
    grafo = graphviz.Source(archivo_dot)
    arbol = grafo.pipe(format='svg')
    arbol = base64.b64encode(arbol).decode('utf-8')
    return render_template('reporte.html', chart=arbol)

@app.route("/tabla")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def table():
    global parsed_tree
    archivo_dot = parsed_tree.crearTabla(parsed_tree)
    grafo = graphviz.Source(archivo_dot)
    tabla = grafo.pipe(format='svg')
    tabla = base64.b64encode(tabla).decode('utf-8')
    return render_template('reporte.html', chart_tabla=tabla)
    

@app.route("/error")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def error():
    global parsed_tree
    archivo_dot = parsed_tree.tablaError(parsed_tree)
    grafo = graphviz.Source(archivo_dot)
    errores = grafo.pipe(format='svg')
    errores = base64.b64encode(errores).decode('utf-8')
    return render_template('reporte.html', chart_error=errores)
if __name__ == "__main__":
    app.run(debug=True)#para que se actualice al detectar cambios