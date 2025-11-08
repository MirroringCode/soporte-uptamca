from app import app
from models import User, Rol
from db import db

def create_admin_user():
    """Crea un usuario administrador con credenciales predeterminadas."""
    with app.app_context():  # Configura el contexto de la aplicación Flask
        # Verificar si ya existe un rol de administrador
        admin_role = Rol.query.filter_by(tipo='Administrador').first()
        if not admin_role:
            admin_role = Rol(id=1, tipo='Administrador')
            db.session.add(admin_role)
            db.session.commit()
            print("Rol 'Administrador' creado.")

        # Verificar si ya existe el usuario administrador
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("El usuario 'admin' ya existe.")
            return

        # Crear el usuario administrador
        admin_user = User(
            username='admin',
            id_rol=admin_role.id
        )
        admin_user.password = 'admin123'  # Establecer la contraseña
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario administrador creado con éxito.")

if __name__ == '__main__':
    create_admin_user()