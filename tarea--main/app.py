from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import data_base_admin as data_base

app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'

# Usuarios de ejemplo
usuarios = {
    "operario1": {"contrasena": hashlib.sha256("op1pass".encode()).hexdigest(), "rol": "operario"},
    "admin1": {"contrasena": hashlib.sha256("admin1pass".encode()).hexdigest(), "rol": "admin"}
}

@app.route('/')
def home():
    if 'usuario' in session:
        rol = session['rol']
        if rol == 'admin':
            return render_template('administrador.html')
        elif rol == 'operario':
            return render_template('operario.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if username in usuarios and usuarios[username]['contrasena'] == password:
            session['usuario'] = username
            session['rol'] = usuarios[username]['rol']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/Crear', methods=['GET'])
def crear():
    return render_template('Crear.html')

@app.route('/Eliminar_usuario', methods=['GET'])
def eliminar():
    return render_template('Eliminar.html')

if __name__ == '__main__':
    app.run(debug=True)


"""from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import hashlib
import data_base_admin as data_base
app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'

usuarios = {
    "operario1": {"contrasena": hashlib.sha256("op1pass".encode()).hexdigest(), "rol": "operario"},
    "admin1": {"contrasena": hashlib.sha256("admin1pass".encode()).hexdigest(), "rol": "admin"}
}

@app.route('/')
def home():
    return render_template('administrador.html')


@app.route('/Eliminar_usuario', methods=['GET'])
def eliminar():
    return render_template('Eliminar.html')


@app.route('/capturar_numero_serie', methods=['POST'])
def eliminar_producto():
    try:
        # Obtener el número de serie del formulario
        numero_serie = request.form['serial-number']
        print(f"Intentando eliminar el producto con número de serie: {numero_serie}")

        # Conexión a la base de datos
        conexion = data_base.conectar()
        print(f"Conexión establecida: {conexion is not None}")

        if conexion is not None:
            # Intentar eliminar el producto
            resultado = data_base.eliminar_producto(conexion, numero_serie)
            print(f"Resultado de la eliminación: {resultado}")

            if resultado:
                print(f"Producto con número de serie {numero_serie} eliminado correctamente")
                return jsonify({"mensaje": "Producto eliminado correctamente"})
            else:
                print(f"No se encontró producto con el número de serie: {numero_serie}")
                return jsonify({"error": "No se encontró producto con el número de serie proporcionado"})
        else:
            print("Error: No se pudo conectar a la base de datos")
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return jsonify({"error": str(e)})
@app.route('/Crear', methods=['GET'])
def Crear():
    return render_template('Crear.html')
@app.route('/crear_usuario', methods=['POST'])
def crear_producto():
    try:
        # Capturar los datos del formulario
        product_id = request.form['product-id']
        model = request.form['model']
        serial_number = request.form['serial-number']
        defect = request.form['defect']

        print(f"Datos recibidos: {product_id}, {model}, {serial_number}, {defect}")

        # Conexión a la base de datos
        conexion = data_base.conectar()

        if conexion:
            # Insertar el producto en la base de datos
            resultado = data_base.crear_producto(conexion, product_id, model, serial_number, defect)
            if resultado:
                print("Producto creado exitosamente.")
                return jsonify({"mensaje": "Producto creado exitosamente"}), 200
            else:
                print("Error al crear el producto.")
                return jsonify({"error": "Error al crear el producto"}), 500
        else:
            print("Error de conexión a la base de datos.")
            return jsonify({"error": "Error de conexión a la base de datos"}), 500

    except Exception as e:
        print(f"Error al crear el producto: {e}")
        return jsonify({"error": "Ocurrió un error al procesar el formulario"}), 500



if __name__ == '__main__':
    app.run(debug=True)"""