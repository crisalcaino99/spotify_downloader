from flask import Flask, render_template, request, redirect
from main3 import ver_playlists, watch_playlists

app = Flask(__name__, static_url_path='/favicon', static_folder='favicon')

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["user_input"]
        playlists = ver_playlists(username)
        return render_template('result.html', nombre_usuario=username, playlists=playlists)
    return render_template('index.html')

@app.route("/llamar_funcion_backend", methods=["POST"])
def llamar_funcion_backend():
    datos = request.get_json()
    
    # Realiza alguna lógica basada en los datos, como procesamiento o almacenamiento
    # ...

    # Redirige a la página result_2.html después de procesar la solicitud
    return redirect('/result_2')

@app.route('/result_2', methods=["GET"])
def result_2():
    # Puedes acceder a los datos de la solicitud anterior si es necesario
    # Información específica de la playlist está disponible en request.json
    playlist_id = request.json.get("playlist_id", "")
    playlist_name = request.json.get("playlist_name", "")
    nombre_usuario = request.json.get("nombre_usuario", "")
    
    # Realiza alguna lógica basada en los datos si es necesario
    # ...

    # Renderiza la plantilla result_2.html
    return render_template('result_2.html', playlist_id=playlist_id, playlist_name=playlist_name, nombre_usuario=nombre_usuario)



if __name__ == '__main__':
    app.run(debug=True)



