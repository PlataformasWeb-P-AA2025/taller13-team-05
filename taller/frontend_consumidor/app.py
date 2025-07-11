# frontend_consumidor/app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json 


app = Flask(__name__,
            template_folder='templates', 
            static_folder='static')     


app.secret_key = 'tu_clave_secreta_muy_segura_aqui_CAMBIAME_POR_FAVOR' 


API_BASE_URL = "http://127.0.0.1:8000/api" 


API_TOKEN = "ab2a8f0bbfe76f08fe1be73e61c1284219709044"  

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json" 
}

def _make_api_request(method, endpoint, data=None):
    api_url = f"{API_BASE_URL}/{endpoint}/"
    response = None 
    try:
        if method == 'GET':
            response = requests.get(api_url, headers=headers)
        elif method == 'POST':
            response = requests.post(api_url, json=data, headers=headers)
        
        response.raise_for_status() 
        return response.json(), None 

    except requests.exceptions.ConnectionError as e:
        return None, f"Error de conexión con la API: Asegúrate de que el servidor de Django esté corriendo en {API_BASE_URL}. Detalles: {e}"
    except requests.exceptions.RequestException as e:
        error_msg = f"Error en la petición a la API: {e}"
        if response is not None:
            try:
                error_details = response.json()
                error_msg += f". Detalles de la API: {error_details}"
            except ValueError:
                error_msg += f". Respuesta de la API: {response.text}"
        return None, error_msg

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/edificios")
def listar_edificios():
    api_url = f"{API_BASE_URL}/edificios/"  
    response = None 
    try: 
        response = requests.get(api_url, headers=headers) 
        response.raise_for_status()  
        
        datos = response.json()
        edificios = datos.get('results', [])  
        num_edificios = datos.get('count', 0) 
        
    except requests.exceptions.ConnectionError as e:
        flash(f"Error de conexión con la API: Asegúrate de que el servidor de Django esté corriendo en {API_BASE_URL}. Detalles: {e}", "danger")
        edificios = []
        num_edificios = 0
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al cargar edificios de la API: {e}"
        if response is not None:
            try:
                error_details = response.json()
                error_msg += f". Detalles de la API: {error_details}"
            except ValueError:
                error_msg += f". Respuesta de la API: {response.text}"
        flash(error_msg, "danger")
        edificios = []
        num_edificios = 0

    return render_template("los_edificios.html", 
                           edificios=edificios, 
                           numero_edificios=num_edificios)

@app.route("/crear-edificio", methods=['GET', 'POST'])
def crear_edificio():
    response = None  
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo']

        edificio_data = {
            'nombre': nombre,
            'direccion': direccion,
            'ciudad': ciudad,
            'tipo': tipo
        }
        
        api_url = f"{API_BASE_URL}/edificios/"
        
        try: 
            response = requests.post(api_url, json=edificio_data, headers=headers)
            response.raise_for_status() 
            
            flash('Edificio creado exitosamente!', 'success')
            return redirect(url_for('listar_edificios'))

        except requests.exceptions.RequestException as e:
            error_msg = f"Error al crear el edificio: {e}"
            if response is not None:
                try:
                    error_details = response.json()
                    error_msg += f". Detalles de la API: {error_details}"
                except ValueError:
                    error_msg += f". Respuesta de la API: {response.text}"
            flash(error_msg, 'danger')

    return render_template("crear_edificio.html")

def obtener_nombre_edificio(url):
    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['nombre']
    except requests.exceptions.RequestException:
        return "Edificio no encontrado"

@app.route("/departamentos")
def listar_departamentos():
    api_url = f"{API_BASE_URL}/departamentos/"
    
    response = None 
    try: 
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        datos_crudos = response.json().get('results', [])
        num_departamentos = response.json().get('count', 0)
        
        departamentos_procesados = []
        for d in datos_crudos:
            d['edificio_nombre'] = obtener_nombre_edificio(d['edificio'])
            departamentos_procesados.append(d)

    except requests.exceptions.ConnectionError as e:
        flash(f"Error de conexión con la API: Asegúrate de que el servidor de Django esté corriendo en {API_BASE_URL}. Detalles: {e}", "danger")
        departamentos_procesados = []
        num_departamentos = 0
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al cargar departamentos de la API: {e}"
        if response is not None:
            try:
                error_details = response.json()
                error_msg += f". Detalles de la API: {error_details}"
            except ValueError:
                error_msg += f". Respuesta de la API: {response.text}"
        flash(error_msg, "danger")
        departamentos_procesados = []
        num_departamentos = 0

    return render_template("los_departamentos.html", 
                           departamentos=departamentos_procesados, 
                           numero_departamentos=num_departamentos)
    
@app.route("/crear-departamento", methods=['GET', 'POST'])
def crear_departamento():
    edificios_disponibles = []
    response = None 
    try: 
        edificios_api_url = f"{API_BASE_URL}/edificios/"
        response = requests.get(edificios_api_url, headers=headers)
        response.raise_for_status()
        edificios_disponibles = response.json().get('results', [])
    except requests.exceptions.ConnectionError as e:
        flash(f"Error de conexión al cargar edificios para el formulario: {e}", "danger")
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al cargar la lista de edificios para el formulario: {e}"
        if response is not None:
            try:
                error_details = response.json()
                error_msg += f". Detalles de la API: {error_details}"
            except ValueError:
                error_msg += f". Respuesta de la API: {response.text}"
        flash(error_msg, "danger")

    if request.method == 'POST':
        propietario = request.form['propietario']
        
        try:
            costo = float(request.form['costo'])
            num_cuartos = int(request.form['num_cuartos'])
        except ValueError:
            flash("Error: El costo y el número de cuartos deben ser números válidos.", "danger")
            return render_template("crear_departamento.html", edificios=edificios_disponibles)
            
        edificio_url = request.form['edificio']

        departamento_data = {
            'propietario': propietario,
            'costo': costo,
            'num_cuartos': num_cuartos,
            'edificio': edificio_url 
        }
        
        api_url = f"{API_BASE_URL}/departamentos/"
        
        response = None 
        try: 
            response = requests.post(api_url, json=departamento_data, headers=headers)
            response.raise_for_status()
            
            flash('Departamento creado exitosamente!', 'success')
            return redirect(url_for('listar_departamentos'))

        except requests.exceptions.RequestException as e:
            error_msg = f"Error al crear el departamento: {e}"
            if response is not None:
                try:
                    error_details = response.json()
                    error_msg += f". Detalles de la API: {error_details}"
                except ValueError:
                    error_msg += f". Respuesta de la API: {response.text}"
            flash(error_msg, 'danger')

    return render_template("crear_departamento.html", edificios=edificios_disponibles)

if __name__ == '__main__':
    app.run(debug=True)