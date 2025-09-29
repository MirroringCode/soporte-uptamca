from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Inicialización de la aplicación Flask
app = Flask(__name__)
CORS(app) # Habilita CORS para permitir la comunicación con el frontend

# --- CONFIGURACIÓN DE LA CONEXIÓN A MYSQL ---
# ¡IMPORTANTE! Reemplaza estos valores con los de tu base de datos.
db_config = {
    'host': 'localhost',
    'user': 'root', # Tu usuario de MySQL
    'password': '', # Tu contraseña de MySQL
    'database': 'soportes-uptamca' # El nombre de tu base de datos
}

# --- ENDPOINTS DE LA API ---

@app.route('/verify-user', methods=['POST'])
def verify_user():
    """Verifica al usuario contra las tablas 'personal' y 'departamentos'."""
    data = request.get_json()
    full_name = data.get('fullName', '')
    department_name = data.get('department', '')

    # Asumimos que el nombre completo viene como "Nombre Apellido"
    name_parts = full_name.split(' ', 1)
    first_name = name_parts[0] if len(name_parts) > 0 else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    # Consulta SQL ajustada a tu esquema: personal(Id, nombre, apellido, id_departamente), departamentos(id, nombre)
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
            # Si se encuentra, devolvemos el ID del personal y el ID del departamento
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


@app.route('/log-ticket', methods=['POST'])
def log_ticket():
    """Registra un nuevo ticket en la tabla 'soportes'."""
    data = request.get_json()
    employee_id = data.get('employeeId')
    department_id = data.get('departmentId')
    problem_type = data.get('problemType')
    status = data.get('status') # 'resolved' o 'escalated'

    # El estado 'atendido' será 0 (falso) si el ticket se está escalando
    atendido_status = 0 if status == 'escalated' else 1

    # Obtenemos la fecha y hora actual
    current_timestamp = datetime.now()

    # Consulta SQL ajustada a tu tabla 'soportes'
    query = """
        INSERT INTO soportes (motivo, atendido, id_personal, id_departamentos, fecha) 
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, (problem_type, atendido_status, employee_id, department_id, current_timestamp))
        conn.commit()

        return jsonify({'success': True, 'ticketId': cursor.lastrowid})

    except Error as e:
        print(f"Error en /log-ticket: {e}")
        return jsonify({'success': False, 'message': 'Error al registrar el ticket.'}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Iniciar el servidor
if __name__ == '__main__':
    app.run(port=3000, debug=True)