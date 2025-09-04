from sqlalchemy.dialects.mysql import INTEGER
from db import db


class User(db.Model):
    """ Define propiedades que tendran los usuarios al usarse en el Sistema.
    Basicamente es una representación de la tabla existente en base de datos, 
    pero en codigo, para usarse en el programa
    """

    __tablename__ = 'user' # Nombre de la tabla

    # Campos dentro de la tabla (deben coincidir con los que están creados en el MySQL)
    id            = db.Column(INTEGER(unsigned=True), primary_key=True)
    username      = db.Column(db.String(255), nullable=False)
    id_rol        = db.Column(INTEGER(unsigned=True), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Metodo para jalar lista de usuarios
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'id_rol': self.id_rol,
        }   
    
    def __repr__(self):
        return f'<Usuario {self.username}>'



class Rol(db.Model):
    """ Representación dentro de sistema de la tabla 'rol' """
    __tablename__ = 'rol' # Nombre de la tabla

    # campos dentro de la tabla
    id   = db.Column(INTEGER(unsigned=True), primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)

    # Jalar lista de roles
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo
        }
    
    def __repr__(self):
        return f'<rol {self.tipo}'



class Personal(db.Model):
    """ Representación dentro del sistema de la tabla 'personal' """
    __tablename__ = 'personal'

    # campos dentro de la tabla
    id              = db.Column(INTEGER(unsigned=True), primary_key=True)
    cedula          = db.Column(db.String(100), nullable=False)
    nombre          = db.Column(db.String(255), nullable=False)
    apellido        = db.Column(db.String(255), nullable=False)
    id_departamento = db.Column(INTEGER(unsigned=True), nullable=False)

    # Jalar lista de personal
    def to_dict(self):
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'id_departamento': self.id_departamento
        }

    def __repr__(self):
        return f'<Personal {self.nombre} {self.apellido}>'


class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id     = db.Column(INTEGER(unsigned=True), primary_key=True)
    nombre = db.Column(INTEGER(unsigned=True), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }


# class Soporte(db.Model):
#     __tablename__ = 'soportes'




