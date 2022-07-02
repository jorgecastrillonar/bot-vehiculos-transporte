import database.db as db
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Revision(db.Base):
    __tablename__ = 'revision'
     
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    nivel_aceite = Column('nivel_aceite', String(10), nullable=False)
    nivel_liquido_frenos = Column('nivel_liquido_frenos', String(10), nullable=False)
    nivel_refrigerante = Column('nivel_refrigerante', String(10), nullable=False)
    nivel_liquido_direccion = Column('nivel_liquido_direccion', String(10), nullable=False)
  
    revisiones_vehiculos = relationship('VehiculoRevision', back_populates='revision')
    
    def __init__(self, nivel_aceite = "",nivel_liquido_frenos="",nivel_refrigerante="",nivel_liquido_direccion="" ):
        self.nivel_aceite = nivel_aceite
        self.nivel_liquido_frenos = nivel_liquido_frenos
        self.nivel_refrigerante = nivel_refrigerante
        self.nivel_liquido_direccion = nivel_liquido_direccion


    