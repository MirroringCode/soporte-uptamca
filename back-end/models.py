from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy import ForeignKey
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """ Define propiedades que tendran los usuarios al usarse en el Sistema.
    Basicamente es una representación de la tabla existente en base de datos, 
    pero en codigo, para usarse en el programa
    """

    __tablename__ = 'user' # Nombre de la tabla

    # Campos dentro de la tabla (deben coincidir con los que están creados en el MySQL)
    id            = db.Column(INTEGER(unsigned=True), primary_key=True)
    username      = db.Column(db.String(255), nullable=False)
    id_rol        = db.Column(INTEGER(unsigned=True),
                              ForeignKey('rol.id', ondelete='RESTRICT'), 
                              nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    rol = db.relationship('Rol', backref='users')
    soportes = db.relationship('Soporte', foreign_keys='Soporte.atendido_por', 
                                     backref='user')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Metodo para jalar lista de usuarios
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'rol': self.rol.tipo if self.rol else None,
            'soportes_realizados': len(self.soportes)
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
    id_departamento = db.Column(INTEGER(unsigned=True),
                                ForeignKey('departamentos.id', ondelete='RESTRICT'), 
                                nullable=False)

    departamento = db.relationship('Departamento', backref='personal')
    soportes_solicitados = db.relationship('Soporte', foreign_keys='Soporte.id_personal',
                                           backref='solicitante')

    # Jalar lista de personal
    def to_dict(self):
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'departamento': self.departamento.nombre if self.departamento else None,
        }

    def __repr__(self):
        return f'<Personal {self.nombre} {self.apellido}>'


class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id     = db.Column(INTEGER(unsigned=True), primary_key=True)
    nombre = db.Column(db.String, nullable=False, unique=True)


    soportes = db.relationship('Soporte', foreign_keys='Soporte.id_departamento',
                               backref='departamento')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }


class Soporte(db.Model):

    __tablename__ = 'soportes'

    id              = db.Column(INTEGER(unsigned=True), primary_key=True)
    motivo          = db.Column(db.String(255), nullable=False)
    atendido        = db.Column(db.Boolean, nullable=False, default=False)
    atendido_por    = db.Column(INTEGER(unsigned=True),
                                ForeignKey('user.id', ondelete='SET NULL'), 
                                nullable=True)
    id_personal     = db.Column(INTEGER(unsigned=True),
                                ForeignKey('personal.id', ondelete='SET NULL'), 
                                nullable=True)
    id_departamento = db.Column(INTEGER(unsigned=True), 
                                ForeignKey('departamentos.id', ondelete='SET NULL'),
                                nullable=True)
    fecha           = db.Column(TIMESTAMP, nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'motivo': self.motivo,
            'atendido': self.atendido,
            'tecnico': self.user.username if self.user else None,
            'solicitante': f'{self.solicitante.nombre} {self.solicitante.apellido}' if self.solicitante else None,
            'departamento': self.departamento.nombre if self.departamento else None,
            'fecha': str(self.fecha)
        }


