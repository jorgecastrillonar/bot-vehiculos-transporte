import database.db as db
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

class TipoVehiculo(db.Base):
    __tablename__ = 'tipo_vehiculo'
     
    id = Column('id', String(15), primary_key=True, nullable=False)
    nombre = Column('nombre', String(25), nullable=False)
    descripcion = Column('descripcion', Text, nullable=False)
    
    
    vehiculos = relationship('Vehiculo', back_populates='tipo_vehiculo')
    
    def __init__(self, id, nombre="", descripcion=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
    
    def __repr__(self):
        return f"<Tipo vehículo {self.id}>"