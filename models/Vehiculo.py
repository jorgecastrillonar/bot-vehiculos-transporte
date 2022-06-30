import database.db as db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Vehiculo(db.Base):
    __tablename__ = 'vehiculo'
     
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    placa = Column('placa', String(6), nullable=False,  unique=True)
    marca = Column('marca', String(25), nullable=False)
    modelo = Column('modelo', Integer, nullable=False)
    #tipo_vehiculo_id = Column('tipo_vehiculo_id', String(15), ForeignKey('tipo_vehiculo.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    #tipo_vehiculo = relationship('TipoVehiculo', back_populates='vehiculos')
    
    def __init__(self, placa="", marca = "", modelo = 0):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
    
    def __repr__(self):
        return f"<Vehículo {self.placa}>"