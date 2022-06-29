import database.db as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import relationship


class Usuario(db.Base):

    __tablename__ = 'usuario'

    id = Column('id', String(15), primary_key=True, nullable=False)
    documento_identidad = Column('documento_identidad', Integer(), server_default='0', nullable=False)
    nombre_completo = Column('nombre_completo', String(50), server_default='0', nullable=True)
    tipo_usuario_id = Column('tipo_usuario_id', String(15), ForeignKey('tipo_usuario.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    tipo_usuario_id = relationship("TipoUsuario", back_populates="usuario")
    
    def __init__(self, id, documento_identidad, nombre_completo, tipo_usuario_id):
        self.id = id
        self.documento_identidad = documento_identidad
        self.nombre_completo = nombre_completo
        self.tipo_usuario_id = tipo_usuario_id

    def __repr__(self):
        return f"<Usuario {self.id}>"

    