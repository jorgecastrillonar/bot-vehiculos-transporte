import database.db as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Sequence
from sqlalchemy.orm import relationship


class Usuario(db.Base):

    __tablename__ = 'usuario'

    id = Column('id', Integer, primary_key=True, autoincrement=True ,nullable=False)
    documento_identidad = Column('documento_identidad', Integer, server_default='0', nullable=False, unique=True)
    nombre_completo = Column('nombre_completo', String(50), server_default='0', nullable=True)
    tipo_usuario_id = Column('tipo_usuario_id', String(15), ForeignKey('tipo_usuario.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=True)

    tipo_usuario = relationship('TipoUsuario', back_populates='usuarios')
    
    def __init__(self, documento_identidad=0, nombre_completo = "", tipo_usuario_id = ""):
        self.documento_identidad = documento_identidad
        self.nombre_completo = nombre_completo
        self.tipo_usuario_id = tipo_usuario_id

    def __repr__(self):
        return f"<Usuario {self.id}>"

    def almacenar(self):
       db.Base.metadata.create_all(db.engine)
       session = db.Session()
       session.add(self)
       session.commit()
       
    def eliminar(self):
       db.Base.metadata.create_all(db.engine)
       session = db.Session()
       session.query(Usuario).filter(Usuario.id==self.id).delete()
       session.commit()    