from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER

class User(db.Model):
    __tablename__ = 'user'

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    id_rol   = db.Column(INTEGER(unsigned=True), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'id_rol': self.id_rol,
            'password': self.password 
        }   
    
    def __repr__(self):
        return f"<Publicacion {self.username}>"
