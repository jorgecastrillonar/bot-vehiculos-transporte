import database.db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship


class TipoUsuario(db.Base):

    __tablename__ = 'tipo_usuario'

    id = Column('id', String(15), primary_key=True, nullable=False)
    nombre = Column('nombre', String(50), server_default='0', nullable=False)
    descripcion = Column('descripcion', String(50), server_default='0', nullable=False)
    
    usuario = relationship("Usuario", back_populates="tipo_usuario")
    
    def __init__(self, id, nombre, descripcion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f"<TipoUsuario {self.id}>"
