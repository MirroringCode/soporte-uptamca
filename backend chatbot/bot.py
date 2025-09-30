from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE LA CONEXIÓN A MYSQL ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'soportes-uptamca'
}

# --- ENDPOINTS DE LA API ---

@app.route('/verify-user', methods=['POST'])
def verify_user():
    # ... (esta función se mantiene exactamente igual que antes) ...
    data = request.get_json()
    full_name = data.get('fullName', '')
    department_name = data.get('department', '')

    name_parts = full_name.split(' ', 1)
    first_name = name_parts[0] if len(name_parts) > 0 else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    query = """
        SELECT p.Id, d.id FROM personal p
        JOIN departamentos d ON p.id_departamente = d.id
        WHERE LOWER(p.nombre) = LOWER(%s)
          AND LOWER(p.apellido) = LOWER(%s)
          AND LOWER(d.nombre) = LOWER(%s)
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, department_name))
        result = cursor.fetchone()
        if result:
            employee_id = result[0]
            department_id = result[1]
            return jsonify({'success': True, 'employeeId': employee_id, 'departmentId': department_id})
        else:
            return jsonify({'success': False, 'message': 'Usuario no encontrado. Verifica tus datos.'})
    except Error as e:
        print(f"Error en /verify-user: {e}")
        return jsonify({'success': False, 'message': 'Error en la base de datos.'}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# **NUEVO ENDPOINT PARA CREAR EL TICKET INMEDIATAMENTE**
@app.route('/create-ticket', methods=['POST'])
def create_ticket():
    """Crea un registro inicial en la tabla 'soportes'."""
    data = request.get_json()
    employee_id = data.get('employeeId')
    department_id = data.get('departmentId')
    problem_type = data.get('problemType') # El motivo del soporte

    # Obtenemos la fecha y hora actual para el campo 'fecha'
    current_timestamp = datetime.now()

    # Consulta para insertar los datos iniciales. 'atendido' y 'atendido_por' quedan con sus valores por defecto.
    query = """
        INSERT INTO soportes (id_personal, id_departamentos, fecha, motivo) 
        VALUES (%s, %s, %s, %s)
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Pasamos los datos que necesita la tabla
        cursor.execute(query, (employee_id, department_id, current_timestamp, problem_type))
        conn.commit()
        # Devolvemos el ID del ticket recién creado
        return jsonify({'success': True, 'ticketId': cursor.lastrowid})
    except Error as e:
        print(f"Error en /create-ticket: {e}")
        return jsonify({'success': False, 'message': 'Error al crear el ticket.'}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# El endpoint /log-ticket ya no lo usaremos para crear, sino para actualizar, pero lo dejamos por si acaso
@app.route('/log-ticket', methods=['POST'])
def log_ticket():
    # ... (esta función se mantiene igual, aunque ahora usaremos la nueva) ...
    # ... (puedes borrarla si quieres para limpiar el código) ...
    pass


if __name__ == '__main__':
    app.run(port=5500, debug=True)