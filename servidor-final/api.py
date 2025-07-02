from flask import Flask, request, jsonify
from models import init_db, insertar_dato, obtener_ultimos_datos

#Crea la aplicacion Flask
app = Flask(__name__)

#Define una ruta que responde a POST /api/datos
@app.route('/api/datos', methods=['POST'])

#Funcion que recibe datos JSON desde el servidor intermedio
def recibir_dato():

    #Toma el mensaje y lo convierte en un diccionario Python
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    #Llama a "insertar_dato()" para guardar el dato en la BD
    try:
        insertar_dato(data)
        return jsonify({'mensaje': 'Dato almacenado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Define una ruta GET /api/datos usada por el Cliente consulta para obtener los ultimos registros
@app.route('/api/datos', methods=['GET'])
def get_datos():

    #Llama a "obtener_ultimos_datos()" para conseguir los ultimos "limit" registros
    #Y los devuelve en JSON
    try:
        datos = obtener_ultimos_datos()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
