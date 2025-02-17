# 🚖 Taxímetro Web

<p align="center">
  <img src="https://github.com/user-attachments/assets/eb3898ee-eca7-4c8d-8c28-becafa44ab00" alt="Logo" width="300">
</p>

Este es el desarrollo web de un taxímetro para el uso de cualquier conductor que lo quiera emplear. Su funcionalidad simple y dinámica le permite, en pocas interacciones, manejar la web con gran versatilidad.

## 📌 Descripción
Este proyecto está enfocado en conductores, permitiéndoles registrar sus trayectos. Según la tarifa seleccionada, al finalizar el recorrido se calculará automáticamente el monto a cobrar al pasajero.

## ✨ Características Principales
- ✅ **Inicio y finalización del taxímetro**
- ✅ **Cálculo del total a pagar** basado en el tiempo en movimiento y en parada
- ✅ **Gestión de tarifas personalizadas**
- ✅ **Historial de recorridos**
- ✅ **Registro de nuevos conductores**

Este proyecto está desarrollado con **Flask** y utiliza **MongoDB** para el almacenamiento de datos.

---

## 🛠 Instalación
### 1️⃣ Clonar el repositorio
```bash
    git clone https://github.com/tuusuario/taximetro.git
    cd taximetro
```
### NOTA: Instalar UV
```bash
    pip install uv 
    cd taximetro
```
### 2️⃣ Crear y activar entorno virtual (`venv`)
```bash
# En Windows:
    python -m venv venv
    venv\Scripts\activate

# En Mac/Linux:
    python3 -m venv venv
    source venv/bin/activate
```
### 3️⃣ Instalar dependencias
```bash
    uv pip install --requirements pyproject.toml
```

### 4️⃣ Configurar MongoDB
Para manejar cada usuario su propia base de datos, se recomienda configurar MongoDB con la URL de conexión en `app.py`:
```python
app.config["MONGO_URI"] = "mongodb+srv://usuario:contraseña@servidor.mongodb.net/TuBaseDeDatos"
```

---

## 🚀 Uso del Proyecto
### 🔹 Iniciar el servidor
Con el entorno `venv` activado, ejecutar:
```bash
    python app.py
```
Acceder desde el navegador a: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 🔹 Rutas Principales
| Ruta         | Descripción  |
|-------------|-------------|
| `/`         | Página principal |
| `/login`    | Iniciar sesión |
| `/register` | Registro de nuevos conductores |
| `/tarifas`  | Gestión de tarifas |
| `/recorridos` | Historial de recorridos |

### 🔹 Uso del Taxímetro
1. Presionar el botón **"Iniciar Taxímetro"**.
2. Conducir usando las teclas numéricas:
   - **7** → Girar a la izquierda
   - **8** → Avanzar recto
   - **9** → Girar a la derecha
3. Para detenerse, basta con no tocar ninguna tecla.
4. Para finalizar el trayecto, presionar **"Finalizar Taxímetro"**.
   - Se mostrarán todos los datos del trayecto y el monto a cobrar.
5. Para **iniciar un nuevo recorrido**, presionar nuevamente **"Iniciar Taxímetro"**.

### 🔹 Cambio de Tarifa
1. Ir al menú y seleccionar **"Tarifas"**.
2. Elegir una tarifa y hacer clic en **"Actualizar Tarifa"**.
3. Se mostrará una alerta confirmando la actualización.

---

## 🏗 Tecnologías Utilizadas

- 🐍 **Flask** (Backend)
- 🗄 **MongoDB** (Base de datos NoSQL)
- 🎨 **HTML + CSS** (Interfaz de usuario)
- 📡 **JavaScript (fetch API)** (Comunicación cliente-servidor)

---

## 👥 Contribuciones
Si quieres colaborar en este proyecto, ¡serás bienvenido! Puedes abrir un _issue_ o enviar un _pull request_ con mejoras.

--- 
## 📚 enlaces
- Primer git con todos los commit : https://github.com/mr-melenas/ejercicios/tree/main/taximetro .
- JIRA: https://mbeltranestudio.atlassian.net/jira/software/projects/SCRUM/boards/1
---


🚀 ¡Esperamos que este taxímetro te sea útil en tu día a día como conductor!
