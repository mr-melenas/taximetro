from flask import Flask, render_template, request, redirect, url_for ,session, flash, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secreto_super_seguro'  # Clave para manejar sesiones

tarifa_seleccionada = None  # Clave para ma

# Conectar a MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://user:pass@serv.mongodb.net/ruta"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


#----------------------------------------------------------------------------------------------------------------------------
# prueba test BD
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/test-connection')
def test_connection():
    try:
        # Intentar acceder a la colección 'conductores'
        mongo.db.conductores.find_one()
        return "✅ Conexión a MongoDB exitosa."
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"


#----------------------------------------------------------------------------------------------------------------------------
# Página de registro
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username'].strip()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        telefono = request.form.get('telefono', '').strip()  # Opcional
        matricula = request.form.get('matricula', '').strip()  # Opcional

        # Verificar si el usuario ya existe
        if mongo.db.conductores.find_one({'username': username}):
            flash('El usuario ya existe. Intenta con otro.', 'danger')
            return redirect(url_for('register'))
        
        # Verificar si el email ya existe
        if mongo.db.conductores.find_one({'email': email}):
                flash('El correo electrónico ya está registrado.', 'danger')
                return redirect(url_for('register'))
        
        nuevo_usuario = {
            'username': username,
            'password': password,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono if telefono else None,
            'matricula': matricula if matricula else None,
            'tipo': "tarifa_estandar"
        }

        # Insertar el nuevo usuario en la colección 'conductores'
        mongo.db.conductores.insert_one(nuevo_usuario)
        flash('¡Registro exitoso! Ahora inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



#----------------------------------------------------------------------------------------------------------------------------
# Página de login y logout
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = mongo.db.conductores.find_one({'username': username})

        if usuario and bcrypt.check_password_hash(usuario['password'], password):
            session['usuario'] = username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))  # Redirige para que el mensaje se muestre

    return render_template('login.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))


#----------------------------------------------------------------------------------------------------------------------------
# Página principal
#----------------------------------------------------------------------------------------------------------------------------
# Página principal (requiere login)
@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

@app.route('/iniciar_taximetro', methods=['POST'])
def iniciar_taximetro():
    #print("entro en iniciar_taximetro")
    session['start_time'] = datetime.now()
    session['tiempo_movimiento'] = 0  # Reiniciar tiempo de movimiento
    session['tiempo_parado'] = 0      # Reiniciar tiempo parado
    return jsonify({"status": "Taxímetro iniciado"})

@app.route('/finalizar_taximetro', methods=['POST'])
def finalizar_taximetro():
    if 'usuario' not in session:
        return jsonify({"error": "Usuario no autenticado"}), 403

    data = request.get_json()
    usuario = mongo.db.conductores.find_one({'username': session['usuario']})
    tarifa = mongo.db.tarifas.find_one({'tipo': usuario['tipo']})
    if not tarifa:
        return jsonify({"error": "Tarifa no encontrada para el usuario"}), 404
    
    precio_parado= tarifa['parado']
    precio_movimiento= tarifa['movimiento']
    tiempo_total = data['tiempo_total']
    tiempo_movimiento = 0
    tiempo_parado = 0
    tiempo_movimiento = data['tiempo_movimiento']
    tiempo_parado = max(0, tiempo_total - tiempo_movimiento)  # Evitar valores negativos
    total_pagar = tiempo_parado * precio_parado + tiempo_movimiento * precio_movimiento
    print(f"tiempo_parado {tiempo_parado}")
    print(f"tiempo_movimiento {tiempo_movimiento}")
    print(f"tiempo_total {tiempo_total} ")
    print(f"total_pagar {total_pagar:.2f}€")
    # Guardar en MongoDB
    mongo.db.recorridos.insert_one({
        "conductor": session.get('usuario'),
        "tiempo_total": tiempo_total,
        "tiempo_parado": tiempo_parado,
        "tiempo_movimiento": tiempo_movimiento,
        "total_pagar": total_pagar,
        "fecha_registro": datetime.now(),
        "tarifa": usuario['tipo'] #guardo en bd el tipo de tarifa
    })

    return jsonify({
        "conductor": session.get('usuario'),
        "tiempo_total": tiempo_total,
        "tiempo_movimiento": tiempo_movimiento,
        "tiempo_parado": tiempo_parado,
        "total_pagar": total_pagar
    })

# Ruta para guardar un recorrido
@app.route('/guardar_recorrido', methods=['POST'])
def guardar_recorrido():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    print("entro en guardar_recorrido!!!!!!!!!!!!!")
    data = request.form
    nuevo_recorrido = {
        "conductor": data["conductor"],
        "tiempo_total": int(data["tiempo_total"]),
        "tiempo_parado": int(data["tiempo_parado"]),
        "tiempo_movimiento": int(data["tiempo_movimiento"]),
        "total_pagar": float(data["total_pagar"]),
        "fecha_registro": datetime.now()
    }
    mongo.db.recorridos.insert_one(nuevo_recorrido)
    flash('¡Recorrido guardado con éxito!', 'success')
    return redirect(url_for('mostrar_recorridos'))


#----------------------------------------------------------------------------------------------------------------------------
# Página recorridos
#----------------------------------------------------------------------------------------------------------------------------
# Ruta para ver los recorridos
@app.route('/recorridos')
def mostrar_recorridos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    recorridos = mongo.db.recorridos.find({'conductor': session['usuario']})
    return render_template('recorridos.html', recorridos=recorridos, usuario=session['usuario'])


#----------------------------------------------------------------------------------------------------------------------------
# Página de Tarifas
#----------------------------------------------------------------------------------------------------------------------------
@app.route('/api/tarifas', methods=['GET'])
def obtener_tarifas():
    tarifas = list(mongo.db.tarifas.find({}, {"_id": 0}))  # Excluir el _id
    return jsonify(tarifas)


@app.route('/tarifas')
def tarifas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    tarifas = list(mongo.db.tarifas.find({}, {"_id": 0})) #toma el listado de todas las tarifas
    return render_template('tarifas.html', tarifas=tarifas, usuario=session['usuario'])

@app.route('/actualizar_tarifa', methods=['POST'])
def actualizar_tarifa():
    if 'usuario' not in session:
        return jsonify({"error": "Usuario no autenticado"}), 403

    data = request.get_json()
    nueva_tarifa = data.get('tipo')

    resultado = mongo.db.conductores.update_one(
        {"username": session['usuario']},
        {"$set": {"tipo": nueva_tarifa}}
    )

    if resultado.modified_count > 0:
        return jsonify({"mensaje": "Tarifa actualizada correctamente"})
    else:
        return jsonify({"mensaje": "No se realizó ningún cambio"})


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

# Mostrar todas las rutas registradas por Flask
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)

